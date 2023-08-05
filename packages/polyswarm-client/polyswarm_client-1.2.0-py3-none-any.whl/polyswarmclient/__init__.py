import aiohttp
import asyncio
import base58
import json
import logging
import os
import sys
import time
import websockets

from polyswarmclient import events
from polyswarmclient.balanceclient import BalanceClient
from polyswarmclient.bountiesclient import BountiesClient
from polyswarmclient.stakingclient import StakingClient
from polyswarmclient.offersclient import OffersClient
from polyswarmclient.relayclient import RelayClient
from polyswarmclient.utils import asyncio_join, asyncio_stop, exit, MAX_WAIT
from urllib.parse import urljoin

from web3 import Web3

w3 = Web3()

logger = logging.getLogger(__name__)  # Initialize logger
REQUEST_TIMEOUT = 300.0
MAX_ARTIFACTS = 256


class NonceManager:
    """
    Manages the nonce for some ethereum chain
    """

    def __init__(self, client, chain):
        self.base_nonce = 0
        self.client = client
        self.chain = chain
        self.needs_update = False
        self.nonce_lock = asyncio.Lock()
        self.in_progress = 0
        self.in_progress_condition = asyncio.Condition()

    async def acquire(self):
        """
        Acquires the nonce lock.
        Updates base_nonce if needs_update is set
        """
        await self.nonce_lock.acquire()
        if self.needs_update:
            async with self.in_progress_condition:
                # The wait inside here will release this lock, allowing finished() to work
                await self.in_progress_condition.wait_for(self.all_finished)
            nonce = await self.client.update_base_nonce(self.chain)
            logger.info('Updated to %s', nonce)
            self.needs_update = False
            if nonce is not None:
                self.base_nonce = nonce

    def all_finished(self):
        """
        Check that all tasks have finished
        """
        return self.in_progress == 0

    async def finished(self):
        """
        Mark that some in-progress transaction finished on polyswarmd
        """
        async with self.in_progress_condition:
            self.in_progress -= 1
            self.in_progress_condition.notify()

    async def next(self, amount=1):
        """
        Grab the next amount nonces.

        Args:
            amount (int): amount of sequential nonces to be claimed
        Returns
            (list[int]): a list of nonces to use
        """
        results = []
        async with self:
            for x in range(0, amount):
                results.append(self.base_nonce + x)
            self.base_nonce += amount
            # Inside nonce_lock so that there is no way the next acquire could miss an in progress
            async with self.in_progress_condition:
                # note that a set of nonces is being used
                self.in_progress += 1
        return results

    def mark_update_nonce(self):
        """
        Call this when the nonce is out of sync.
        This sets the update flag to true.
        The next acquire after being set will trigger an update
        """
        self.needs_update = True

    async def __aenter__(self):
        await self.acquire()

    async def __aexit__(self, exc_type, exc, tb):
        self.nonce_lock.release()


def check_response(response):
    """Check the status of responses from polyswarmd

    Args:
        response: Response dict parsed from JSON from polyswarmd
    Returns:
        (bool): True if successful else False
    """
    status = response.get('status')
    ret = status and status == 'OK'
    if not ret:
        logger.error('Received unexpected failure response from polyswarmd', extra={'extra': response})
    return ret


def is_valid_ipfs_uri(ipfs_uri):
    """
    Ensure that a given ipfs_uri is valid by checking length and base58 encoding.

    Args:
        ipfs_uri (str): ipfs_uri to validate

    Returns:
        bool: is this valid?
    """
    # TODO: Further multihash validation
    try:
        return len(ipfs_uri) < 100 and base58.b58decode(ipfs_uri)
    except TypeError:
        logger.error('Invalid IPFS URI: %s', ipfs_uri)
    except Exception as err:
        logger.exception('Unexpected error: %s', err)
    return False


class Client(object):
    """
    Client to connected to a ethereum wallet as well as a pollyswarm_d instance.

    Args:
        polyswarmd_addr (str): URI of polyswarmd you are referring to.
        keyfile (str): Keyfile filename.
        password (str): Password associated with Keyfile.
        api_key (str): Your PolySwarm API key.
        tx_error_fatal (bool): Transaction errors are fatal and exit the program
        insecure_transport (bool): Allow insecure transport such as HTTP?
    """

    def __init__(self, polyswarmd_addr, keyfile, password, api_key=None, tx_error_fatal=False,
                 insecure_transport=False):
        if api_key and insecure_transport:
            raise ValueError('Refusing to send API key over insecure transport')

        protocol = 'http://' if insecure_transport else 'https://'
        self.polyswarmd_uri = protocol + polyswarmd_addr
        self.api_key = api_key

        self.tx_error_fatal = tx_error_fatal
        self.params = {}

        with open(keyfile, 'r') as f:
            self.priv_key = w3.eth.account.decrypt(f.read(), password)

        self.account = w3.eth.account.privateKeyToAccount(self.priv_key).address
        logger.info('Using account: %s', self.account)

        self.__session = None

        # Do not init nonce manager here. Need to wait until we can guarantee that our event loop is set.
        self.nonce_manager = {}

        self.__schedule = {
            'home': events.Schedule(),
            'side': events.Schedule(),
        }

        self.tries = 0

        self.bounties = None
        self.staking = None
        self.offers = None
        self.relay = None
        self.balances = None

        # Events from client
        self.on_run = events.OnRunCallback()

        # Events from polyswarmd
        self.on_new_block = events.OnNewBlockCallback()
        self.on_new_bounty = events.OnNewBountyCallback()
        self.on_new_assertion = events.OnNewAssertionCallback()
        self.on_reveal_assertion = events.OnRevealAssertionCallback()
        self.on_new_vote = events.OnNewVoteCallback()
        self.on_quorum_reached = events.OnQuorumReachedCallback()
        self.on_settled_bounty = events.OnSettledBountyCallback()
        self.on_initialized_channel = events.OnInitializedChannelCallback()

        # Events scheduled on block deadlines
        self.on_reveal_assertion_due = events.OnRevealAssertionDueCallback()
        self.on_vote_on_bounty_due = events.OnVoteOnBountyDueCallback()
        self.on_settle_bounty_due = events.OnSettleBountyDueCallback()

    def run(self, chains=None):
        """
        Run the main event loop

        Args:
            chains (set(str)): Set of chains to operate on. Defaults to {'home', 'side'}
        """
        if chains is None:
            chains = {'home', 'side'}

        while True:
            loop = asyncio.SelectorEventLoop()

            # Default event loop does not support pipes on Windows
            if sys.platform == 'win32':
                loop = asyncio.ProactorEventLoop()

            asyncio.set_event_loop(loop)

            try:
                asyncio.get_event_loop().run_until_complete(self.run_task(chains))
            except asyncio.CancelledError:
                logger.info('Clean exit requested, exiting')

                asyncio_join()
                exit(0)
            except Exception:
                logger.exception('Unhandled exception at top level')
                asyncio_stop()
                asyncio_join()

                self.tries += 1
                wait = min(MAX_WAIT, self.tries * self.tries)

                logger.critical('Detected unhandled exception, sleeping for %s seconds then resetting task', wait)
                time.sleep(wait)
                continue

    async def run_task(self, chains=None):
        """
        How the event loop handles running a task.

        Args:
            chains (set(str)): Set of chains to operate on. Defaults to {'home', 'side'}
        """
        if chains is None:
            chains = {'home', 'side'}
        if self.api_key and not self.polyswarmd_uri.startswith('https://'):
            raise Exception('Refusing to send API key over insecure transport')

        self.params = {'account': self.account}
        # We can now create our locks, because we are assured that the event loop is set
        self.nonce_manager = {'home': NonceManager(self, 'home'), 'side': NonceManager(self, 'side')}
        try:
            # XXX: Set the timeouts here to reasonable values, probably should be configurable
            # No limits on connections
            conn = aiohttp.TCPConnector(limit=0, limit_per_host=0)
            timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            async with aiohttp.ClientSession(connector=conn, timeout=timeout) as self.__session:
                self.bounties = BountiesClient(self)
                self.staking = StakingClient(self)
                self.offers = OffersClient(self)
                self.relay = RelayClient(self)
                self.balances = BalanceClient(self)

                for chain in chains:
                    nonce_manager = self.nonce_manager[chain]
                    async with nonce_manager:
                        nonce_manager.base_nonce = await self.update_base_nonce(chain)
                    await self.bounties.fetch_parameters(chain)
                    await self.staking.fetch_parameters(chain)
                    await self.on_run.run(chain)

                # At this point we're initialized, reset our failure counter and listen for events
                self.tries = 0
                await asyncio.wait([self.listen_for_events(chain) for chain in chains])
        finally:
            self.__session = None
            self.bounties = None
            self.staking = None
            self.offers = None

    async def make_request(self, method, path, chain, json=None, send_nonce=False, api_key=None, tries=2):
        """Make a request to polyswarmd, expecting a json response

        Args:
            method (str): HTTP method to use
            path (str): Path portion of URI to send request to
            chain (str): Which chain to operate on
            json (obj): JSON payload to send with request
            track_nonce (bool): Whether to track generated transaction and update nonce
            api_key (str): Override default API key
            tries (int): Number of times to retry before giving up
        Returns:
            (bool, obj): Tuple of boolean representing success, and response JSON parsed from polyswarmd
        """
        if chain != 'home' and chain != 'side':
            raise ValueError('Chain parameter must be "home" or "side", got {0}'.format(chain))
        if self.__session is None or self.__session.closed:
            raise Exception('Not running')

        uri = urljoin(self.polyswarmd_uri, path)

        params = dict(self.params)
        params['chain'] = chain

        if send_nonce:
            # Set to 0 because I will replace it later
            params['base_nonce'] = 0

        # Allow overriding API key per request
        if api_key is None:
            api_key = self.api_key
        headers = {'Authorization': api_key} if api_key is not None else None

        qs = '&'.join([a + '=' + str(b) for (a, b) in params.items()])
        response = {}
        while tries > 0:
            tries -= 1

            try:
                async with self.__session.request(method, uri, params=params, headers=headers,
                                                  json=json) as raw_response:
                    try:
                        response = await raw_response.json()
                    except (ValueError, aiohttp.ContentTypeError):
                        response = await raw_response.read() if raw_response else 'None'
                        logger.error('Received non-json response from polyswarmd: %s', response)
                        response = {}
                        continue
            except OSError:
                logger.error('Connection to polyswarmd refused, retrying')
            except asyncio.TimeoutError:
                logger.error('Connection to polyswarmd timed out, retrying')

            logger.debug('%s %s?%s', method, path, qs, extra={'extra': response})

            if not check_response(response):
                logger.warning('Request %s %s?%s failed, retrying...', method, path, qs)
                continue
            else:
                break
        if not check_response(response):
            logger.warning('Request %s %s?%s failed, giving up', method, path, qs)
            return False, response.get('errors')

        return True, response.get('result')

    async def post_transactions(self, transactions, chain, api_key=None):
        """Post a set of (signed) transactions to Ethereum via polyswarmd, parsing the emitted events

        Args:
            transactions (List[Transaction]): The transactions to sign and post
            chain (str): Which chain to operate on
            api_key (str): Override default API key

        Returns:
            Response JSON parsed from polyswarmd containing emitted events
        """
        if chain != 'home' and chain != 'side':
            raise ValueError('Chain parameter must be "home" or "side", got {0}'.format(chain))
        if self.__session is None or self.__session.closed:
            raise Exception('Not running')

        signed_txs = [w3.eth.account.signTransaction(tx, self.priv_key) for tx in transactions]
        raw_signed_txs = [bytes(tx['rawTransaction']).hex() for tx in signed_txs]
        success, results = await self.make_request('POST', '/transactions',
                                                   chain,
                                                   json={'transactions': raw_signed_txs},
                                                   api_key=api_key, tries=1)

        if not success:
            if self.tx_error_fatal:
                logger.error('Received fatal transaction error', extra={'extra': results})
                sys.exit(1)
            else:
                logger.error('Received transaction error', extra={'extra': results})

        if len(results) != len(signed_txs):
            logger.warning('Transaction result length mismatch')

        errors = []
        txhashes = []
        for tx, result in zip(signed_txs, results):
            txhash = bytes(tx['hash']).hex()
            message = result.get('message', '')
            is_error = result.get('is_error', False)

            if is_error and 'known transaction' not in message.lower():
                errors.append(message)
            else:
                txhashes.append(txhash)

        route = '/transactions'
        json = {
            'transactions': txhashes
        }
        success, results = await self.make_request('GET', route, chain, json=json,
                                                   api_key=api_key, tries=1)
        if not success:
            if self.tx_error_fatal:
                logger.error('Received fatal transaction error', extra={'extra': results})
                sys.exit(1)
            else:
                logger.error('Received transaction error', extra={'extra': results})

        if not results:
            errors.append('Failed to retrieve transaction results for {}'.format(txhashes))
            return {}

        # Combine errors from transaction post with errors after fetching events
        results['errors'] = errors + results.get('errors', [])
        return results

    def replace_nonce(self, base_nonce, transaction):
        """
        Replaces the nonce in a transaction with the existing nonce value

        Args:
            base_nonce (int): nonce for the wallet being used
            transaction (obj): transaction object from polyswarmd
        Returns
            (list): transactions to be signed and sent
        """
        original = transaction.get('nonce')
        if original is not None:
            transaction['nonce'] = base_nonce
            return transaction

    async def update_base_nonce(self, chain, api_key=None):
        """
        Update account's nonce from polyswarmd

        Args:
            chain (str): Which chain to operate on
            api_key (str): Override default API key
        """
        success, base_nonce = await self.make_request('GET', '/nonce', chain, api_key=api_key)

        if success:
            return base_nonce
        else:
            logger.error('Failed to fetch base nonce')

    async def list_artifacts(self, ipfs_uri, api_key=None):
        """
        Return a list of artificats from a given ipfs_uri.

        Args:
            ipfs_uri (str): IPFS URI to get artifiacts from.
            api_key (str): Override default API key

        Returns:
            List[(str, str)]: A list of tuples. First tuple element is the artifact name, second tuple element
            is the artifact hash.
        """
        if self.__session is None or self.__session.closed:
            raise Exception('Not running')

        if not is_valid_ipfs_uri(ipfs_uri):
            return []

        uri = urljoin(self.polyswarmd_uri, '/artifacts/{0}'.format(ipfs_uri))
        params = dict(self.params)

        # Allow overriding API key per request
        if api_key is None:
            api_key = self.api_key
        headers = {'Authorization': api_key} if api_key is not None else None

        try:
            async with self.__session.get(uri, params=params, headers=headers) as raw_response:
                try:
                    response = await raw_response.json()
                except (ValueError, aiohttp.ContentTypeError):
                    response = await raw_response.read() if raw_response else 'None'
                    logger.error('Received non-json response from polyswarmd: %s', response)
                    return []
        except OSError:
            logger.error('Connection to polyswarmd refused')
            return []
        except asyncio.TimeoutError:
            logger.error('Connection to polyswarmd timed out')
            return []

        logger.debug('GET /artifacts/%s', ipfs_uri, extra={'extra': response})

        if not check_response(response):
            return []

        return [(a['name'], a['hash']) for a in response.get('result', {})]

    async def get_artifact(self, ipfs_uri, index, api_key=None):
        """Retrieve an artifact from IPFS via polyswarmd

        Args:
            ipfs_uri (str): IPFS hash of the artifact to retrieve
            index (int): Index of the sub artifact to retrieve
            api_key (str): Override default API key
        Returns:
            (bytes): Content of the artifact
        """
        if not is_valid_ipfs_uri(ipfs_uri):
            raise ValueError('Invalid IPFS URI')

        uri = urljoin(self.polyswarmd_uri, '/artifacts/{0}/{1}'.format(ipfs_uri, index))
        params = dict(self.params)

        # Allow overriding API key per request
        if api_key is None:
            api_key = self.api_key
        headers = {'Authorization': api_key} if api_key is not None else None

        try:
            async with self.__session.get(uri, params=params, headers=headers) as raw_response:
                if raw_response.status == 200:
                    return await raw_response.read()

                return None
        except OSError:
            logger.error('Connection to polyswarmd refused')
            return None
        except asyncio.TimeoutError:
            logger.error('Connection to polyswarmd timed out')
            return None

    @staticmethod
    def to_wei(amount, unit='ether'):
        return w3.toWei(amount, unit)

    @staticmethod
    def from_wei(amount, unit='ether'):
        return w3.fromWei(amount, unit)

    # Async iterator helper class
    class __GetArtifacts(object):
        def __init__(self, client, ipfs_uri, api_key=None):
            self.i = 0
            self.client = client
            self.ipfs_uri = ipfs_uri
            self.api_key = api_key

        async def __aiter__(self):
            return self

        async def __anext__(self):
            if not is_valid_ipfs_uri(self.ipfs_uri):
                raise StopAsyncIteration

            i = self.i
            self.i += 1

            if i < MAX_ARTIFACTS:
                content = await self.client.get_artifact(self.ipfs_uri, i, api_key=self.api_key)
                if content:
                    return content

            raise StopAsyncIteration

    def get_artifacts(self, ipfs_uri, api_key=None):
        """
        Get an iterator to return artifacts.

        Args:
            ipfs_uri (str): URI where artificats are located
            api_key (str): Override default API key

        Returns:
            `__GetArtifacts` iterator
        """
        if self.__session is None or self.__session.closed:
            raise Exception('Not running')

        return Client.__GetArtifacts(self, ipfs_uri, api_key=api_key)

    async def post_artifacts(self, files, api_key=None):
        """Post artifacts to polyswarmd, flexible files parameter to support different use-cases

        Args:
            files (list[(filename, contents)]): The artifacts to upload, accepts one of:
                (filename, bytes): File name and contents to upload
                (filename, file_obj): (Optional) file name and file object to upload
                (filename, None): File name to open and upload
            api_key (str): Override default API key
        Returns:
            (str): IPFS URI of the uploaded artifact
        """
        with aiohttp.MultipartWriter('form-data') as mpwriter:
            to_close = []
            try:
                for filename, f in files:
                    # If contents is None, open filename for reading and remember to close it
                    if f is None:
                        f = open(filename, 'rb')
                        to_close.append(f)

                    # If filename is None and our file object has a name attribute, use it
                    if filename is None and hasattr(f, 'name'):
                        filename = f.name

                    if filename:
                        filename = os.path.basename(filename)
                    else:
                        filename = "file"

                    payload = aiohttp.payload.get_payload(f, content_type='application/octet-stream')
                    payload.set_content_disposition('form-data', name='file', filename=filename)
                    mpwriter.append_payload(payload)

                uri = urljoin(self.polyswarmd_uri, '/artifacts')
                params = dict(self.params)

                # Allow overriding API key per request
                if api_key is None:
                    api_key = self.api_key
                headers = {'Authorization': api_key} if api_key is not None else None

                async with self.__session.post(uri, params=params, headers=headers, data=mpwriter) as raw_response:
                    try:
                        response = await raw_response.json()
                    except (ValueError, aiohttp.ContentTypeError):
                        response = await raw_response.read() if raw_response else 'None'
                        logger.error('Received non-json response from polyswarmd: %s', response)
                        return None

                logger.debug('POST/artifacts', extra={'extra': response})

                if not check_response(response):
                    return None

                return response.get('result')
            except (OSError, asyncio.TimeoutError):
                logger.error("Artifacts could not be posted, files: %s", files)
            finally:
                for f in to_close:
                    f.close()

    def schedule(self, expiration, event, chain):
        """Schedule an event to execute on a particular block

        Args:
            expiration (int): Which block to execute on
            event (Event): Event to trigger on expiration block
            chain (str): Which chain to operate on
        """
        if chain != 'home' and chain != 'side':
            raise ValueError('Chain parameter must be "home" or "side", got {0}'.format(chain))
        self.__schedule[chain].put(expiration, event)

    async def __handle_scheduled_events(self, number, chain):
        """Perform scheduled events when a new block is reported

        Args:
            number (int): The current block number reported from polyswarmd
            chain (str): Which chain to operate on
        """
        if chain != 'home' and chain != 'side':
            raise ValueError('Chain parameter must be "home" or "side", got {0}'.format(chain))
        while self.__schedule[chain].peek() and self.__schedule[chain].peek()[0] < number:
            exp, task = self.__schedule[chain].get()
            if isinstance(task, events.RevealAssertion):
                asyncio.get_event_loop().create_task(
                    self.on_reveal_assertion_due.run(bounty_guid=task.guid, index=task.index, nonce=task.nonce,
                                                     verdicts=task.verdicts, metadata=task.metadata, chain=chain))
            elif isinstance(task, events.SettleBounty):
                asyncio.get_event_loop().create_task(
                    self.on_settle_bounty_due.run(bounty_guid=task.guid, chain=chain))
            elif isinstance(task, events.VoteOnBounty):
                asyncio.get_event_loop().create_task(
                    self.on_vote_on_bounty_due.run(bounty_guid=task.guid, votes=task.votes,
                                                   valid_bloom=task.valid_bloom, chain=chain))

    async def listen_for_events(self, chain):
        """Listen for events via websocket connection to polyswarmd
        Args:
            chain (str): Which chain to operate on
        """
        if chain != 'home' and chain != 'side':
            raise ValueError('Chain parameter must be "home" or "side", got {0}'.format(chain))
        if not self.polyswarmd_uri.startswith('http'):
            raise ValueError('polyswarmd_uri protocol is not http or https, got {0}'.format(self.polyswarmd_uri))

        # http:// -> ws://, https:// -> wss://
        wsuri = '{0}/events?chain={1}'.format(self.polyswarmd_uri.replace('http', 'ws', 1), chain)
        last_block = 0
        retry = 0
        while True:
            try:
                async with websockets.connect(wsuri) as ws:
                    # Fetch parameters again here so we don't miss update events
                    await self.bounties.fetch_parameters(chain)
                    await self.staking.fetch_parameters(chain)

                    retry = 0
                    while not ws.closed:
                        resp = None
                        try:
                            resp = await ws.recv()
                            resp = json.loads(resp)
                            event = resp.get('event')
                            data = resp.get('data')
                            block_number = resp.get('block_number')
                            txhash = resp.get('txhash')
                        except json.JSONDecodeError:
                            logger.error('Invalid event response from polyswarmd: %s', resp)
                            continue
                        except websockets.exceptions.ConnectionClosed:
                            # Trigger retry logic outside main loop
                            break

                        if event != 'block':
                            logger.info('Received %s on chain %s', event, chain, extra={'extra': data})

                        if event == 'connected':
                            logger.info('Connected to event socket at: %s', data.get('start_time'))
                        elif event == 'block':
                            number = data.get('number', 0)

                            if number <= last_block:
                                continue

                            if number % 100 == 0:
                                logger.debug('Block %s on chain %s', number, chain)

                            asyncio.get_event_loop().create_task(self.on_new_block.run(number=number, chain=chain))
                            asyncio.get_event_loop().create_task(self.__handle_scheduled_events(number, chain=chain))
                        elif event == 'fee_update':
                            d = {'bounty_fee': data.get('bounty_fee'), 'assertion_fee': data.get('assertion_fee')}
                            await self.bounties.parameters[chain].update({k: v for k, v in d.items() if v is not None})
                        elif event == 'bounty':
                            asyncio.get_event_loop().create_task(
                                self.on_new_bounty.run(**data, block_number=block_number, txhash=txhash, chain=chain))
                        elif event == 'assertion':
                            asyncio.get_event_loop().create_task(
                                self.on_new_assertion.run(**data, block_number=block_number, txhash=txhash,
                                                          chain=chain))
                        elif event == 'reveal':
                            asyncio.get_event_loop().create_task(
                                self.on_reveal_assertion.run(**data, block_number=block_number, txhash=txhash,
                                                             chain=chain))
                        elif event == 'vote':
                            asyncio.get_event_loop().create_task(
                                self.on_new_vote.run(**data, block_number=block_number, txhash=txhash, chain=chain))
                        elif event == 'quorum':
                            asyncio.get_event_loop().create_task(
                                self.on_quorum_reached.run(**data, block_number=block_number, txhash=txhash,
                                                           chain=chain))
                        elif event == 'settled_bounty':
                            asyncio.get_event_loop().create_task(
                                self.on_settled_bounty.run(**data, block_number=block_number, txhash=txhash,
                                                           chain=chain))
                        elif event == 'initialized_channel':
                            asyncio.get_event_loop().create_task(
                                self.on_initialized_channel.run(**data, block_number=block_number, txhash=txhash))
                        else:
                            logger.error('Invalid event type from polyswarmd: %s', resp)

            except (OSError, websockets.exceptions.InvalidHandshake):
                logger.error('Websocket connection to polyswarmd refused, retrying')
            except asyncio.TimeoutError:
                logger.error('Websocket connection to polyswarmd timed out, retrying')

            retry += 1
            wait = retry * retry

            logger.error('Websocket connection to polyswarmd closed, sleeping for %s seconds then reconnecting', wait)
            await asyncio.sleep(wait)
