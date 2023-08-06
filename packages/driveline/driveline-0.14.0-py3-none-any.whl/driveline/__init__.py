#  Copyright 2019, 1533 Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import asyncio

import cbor
import logging
import websockets
from concurrent.futures import ThreadPoolExecutor

from .consumers import *
from .exceptions import ClientException
from .id_factory import StreamIdFactory
from .opts import *
from .record_data import *
from .sync import *

log = logging.getLogger('driveline')

MAX_ALIASES = 256


async def retry(fn_coro_or_future, max_retries=0, retry_duration=0.1, exceptions=None):
    exceptions = exceptions or [Exception]
    if max_retries <= 0:
        max_retries = 0x10000000
    retry_count = 0
    while retry_count <= max_retries:
        retry_count += 1
        try:
            return await fn_coro_or_future()
        except tuple(exceptions) as e:
            if retry_count == max_retries:
                raise e
            log.error('caught exception, retrying...')
        time_wait = retry_duration * (2 ^ retry_count - 1) / 2
        log.error('retry[%s]= %ss', retry_count, time_wait)
        await asyncio.sleep(time_wait)


class Stream(AutoSync):
    __slots__ = ['client', 'stream_id']

    def __init__(self, client, stream_id):
        super().__init__()
        self.client = client
        self.stream_id = stream_id

    @synchronous()
    async def append(self, record: any, **options):
        return await self.client.append(self.stream_id, record, **options)

    @synchronous()
    async def close(self):
        return await self.client.close_stream(self)

    @synchronous()
    async def truncate(self):
        return await self.client.truncate(self.stream_id)

    def get_loop(self):
        return self.client.get_loop()


# noinspection PyNoneFunctionAssignment
class DrivelineClient(AutoSync):
    __slots__ = ['consumer_id', 'consumers', 'endpoint', 'is_running', 'loop', 'stream_id_factory', 'ws', 'io_loop']

    def __init__(self, endpoint: str, loop=None):
        super().__init__()
        if loop is None:
            self.loop = asyncio.get_event_loop()
        self.endpoint = endpoint
        self.is_running = False
        self.stream_id_factory = StreamIdFactory(MAX_ALIASES)
        self.consumer_id = 0
        self.consumers = dict()
        self.io_loop = None
        self.ws = None

    @synchronous()
    async def continuous_query(self, dql: str, handler,
                               executor: ThreadPoolExecutor = None, max_concurrency: int = 1, **options) -> Query:

        consumer = Query(self, self._next_consumer_id(), dql, True, handler,
                         executor=executor, max_concurrency=max_concurrency, **options)
        self._register_consumer(consumer)
        await self._query(consumer)
        return consumer.result()

    @synchronous()
    async def query(self, dql: str, handler,
                    executor: ThreadPoolExecutor = None, max_concurrency: int = 1, **options) -> Query:
        consumer = Query(self, self._next_consumer_id(), dql, False, handler,
                         executor=executor, max_concurrency=max_concurrency, **options)
        self._register_consumer(consumer)
        await self._query(consumer)
        return consumer.result()

    async def _query(self, consumer: Query):
        if consumer.is_continuous:
            cmd = 'sq'
        else:
            cmd = 'qq'
        await self._send(cmd, consumer.consumer_id, self._encode_query_options(**consumer.options), consumer.dql)

    def _encode_query_options(self, from_record_id=None, **_options):
        opts = []
        if from_record_id is not None:
            opts.append(TAG_READ_ID)
            opts.append(from_record_id)
        if len(opts) > 0:
            return opts
        else:
            return None

    @synchronous()
    async def cancel(self, query: Query, **_options):
        assert query is not None
        exists = self._unregister_consumer(query)
        if not exists:
            return
        await self._send('can', query.consumer_id, None)

    @synchronous()
    async def append(self, stream: str, record: any, **options):
        assert stream is not None
        await self._send('app', stream, self._encode_append_options(**options), cbor.dumps(record))

    def _encode_append_options(self, **_options):
        return None

    @synchronous()
    async def truncate(self, stream):
        assert stream is not None
        await self._send('trc', None, stream)

    @synchronous()
    async def store(self, key: str, record: any, **options):
        assert key is not None
        await self._send('st', key, self._encode_store_options(**options), cbor.dumps(record))

    def _encode_store_options(self, ttl=None, cas_id=None, **_options):
        opts = []
        if cas_id is not None:
            opts.append(TAG_STORE_CAS_ID)
            opts.append(cas_id)
        if ttl is not None:
            opts.append(TAG_STORE_TTL)
            opts.append(int(ttl))
        if len(opts) > 0:
            return opts
        else:
            return None

    @synchronous()
    async def load(self, key: str, **options):
        consumer = LoadConsumer(self, self._next_consumer_id(), key, **options)
        self._register_consumer(consumer)
        await self._load(consumer)
        return consumer.result()

    async def _load(self, consumer: LoadConsumer):
        await self._send('ld', consumer.consumer_id, self._encode_load_options(**consumer.options), consumer.key)

    def _encode_load_options(self, **_options):
        return None

    async def list_streams(self, stream_pattern: str, **options):
        consumer = ListConsumer(self, self._next_consumer_id(), stream_pattern, **options)
        self._register_consumer(consumer)
        await self._list('sls', consumer)
        return consumer.result()

    async def list_keys(self, keys_pattern: str, **options):
        consumer = ListConsumer(self, self._next_consumer_id(), keys_pattern, **options)
        self._register_consumer(consumer)
        await self._list('lst', consumer)
        return consumer.result()

    async def _list(self, command: str, consumer: ListConsumer):
        await self._send(command, consumer.consumer_id, self._encode_list_options(**consumer.options), consumer.pattern)

    def _encode_list_options(self, **_options):
        return None

    @synchronous()
    async def remove(self, key: str, **options):
        await self._send('rm', self._encode_remove_options(**options), key)

    @synchronous()
    async def remove_matches(self, key_pattern: str, **options):
        await self._send('rmk', self._encode_remove_options(**options), key_pattern)

    def _encode_remove_options(self, **_options):
        return None

    @synchronous()
    async def sync(self):
        consumer = SyncConsumer(self, self._next_consumer_id())
        self._register_consumer(consumer)
        await self._sync(consumer)
        return consumer.result()

    async def _sync(self, consumer: SyncConsumer):
        await self._send('syn', consumer.consumer_id)

    async def _define(self, stream_id, stream_name):
        return await self._send('def', stream_id, stream_name)

    @synchronous()
    async def open_stream(self, stream_name: str):
        assert stream_name is not None
        stream_id, is_alias = self.stream_id_factory.next(stream_name)
        if is_alias:
            await self._define(stream_id, stream_name)
        return Stream(self, stream_id)

    @synchronous()
    def close_stream(self, stream: Stream):
        assert stream is not None
        self.stream_id_factory.release(stream.id)

    @synchronous()
    async def close(self):
        self.is_running = False
        if not self.stopped.done():
            self.stopped.set_result(True)

    def get_loop(self):
        return self.loop

    def _next_consumer_id(self):
        consumer_id = self.consumer_id
        self.consumer_id += 1
        return consumer_id

    def _register_consumer(self, consumer: Consumer):
        self.consumers[consumer.consumer_id] = consumer

    def _unregister_consumer(self, consumer: Consumer):
        try:
            del self.consumers[consumer.consumer_id]
            return True
        except KeyboardInterrupt:
            raise
        except KeyError:
            return False

    async def _connection_did_close(self):
        log.debug('connection did close')
        for consumer in list(self.consumers.values()):
            is_ok = await consumer.on_disconnect()
            if not is_ok:
                self._unregister_consumer(consumer)

    async def _connection_did_connect(self):
        log.debug('connection did connect')
        for stream_id, stream_name in self.stream_id_factory.aliases.items():
            await self._define(stream_id, stream_name)

        for consumer in list(self.consumers.values()):
            is_ok = await consumer.on_reconnect()
            if not is_ok:
                self._unregister_consumer(consumer)

    async def _message_receiver(self, ws):
        log.debug('receiving messages')
        while self.is_running:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=4)
            except websockets.exceptions.ConnectionClosed:
                log.error('connection closed')
                return
            except asyncio.streams.IncompleteReadError:
                # connection failed
                log.exception("failed to read messages")
                return
            except asyncio.TimeoutError:
                log.debug('pinging server')
                # No data in 1 second, check the connection.
                try:
                    pong_waiter = await ws.ping()
                    await asyncio.wait_for(pong_waiter, timeout=1)
                except asyncio.TimeoutError:
                    self.ws = asyncio.Future()
                    raise ConnectionAbortedError('ping failed')
            else:
                try:
                    await self._handle_message(msg)
                except KeyboardInterrupt:
                    raise
                except Exception:
                    log.exception('error processing message')

    async def _handle_message(self, raw_message: bytes):
        msg = cbor.loads(raw_message)
        if len(msg) <= 1:
            log.warning('malformed server message')
            return
        cmd = msg[0]
        if cmd == 'data':
            _, consumer_id, tags, *records = msg
            return await self._dispatch_message(consumer_id, tags=tags, records=records)
        elif cmd == 'err':
            _, consumer_id, error = msg
            return await self._dispatch_message(consumer_id, error=error)
        elif cmd == 'syn':
            _, consumer_id = msg
            return await self._dispatch_message(consumer_id, tags=None, records=[])
        else:
            log.warning('unknown server message')

    async def _dispatch_message(self, consumer_id, **message):
        consumer: Consumer = self.consumers.get(consumer_id)
        if consumer is None:
            log.warning("received data for non-existing consumer id=%s", consumer_id)
            return

        try:
            keep_running = await consumer.on_message(**message)
        except KeyboardInterrupt:
            raise
        except Exception:
            log.exception('error processing message; stopping consumer')
            keep_running = False

        if not keep_running:
            self._unregister_consumer(consumer)

    async def _send(self, *args):
        log.debug('sending message %s', args)
        data = cbor.dumps(args)
        ws = await self.ws
        await ws.send(data)

    async def _run_io_loop(self, started: asyncio.Future):
        connection_opts = dict(
            subprotocols=('driveline',),
            compression=None,
            # read_limit sets the high-water limit of the buffer for incoming bytes
            read_limit=2 ** 10,
            # write_limit sets the high-water limit of the buffer for outgoing bytes
            write_limit=2 ** 10,
            # max_size enforces the maximum size for incoming messages in bytes
            max_size=None,  # 2 ** 20,
            # max_queue sets the maximum length of the queue that holds incoming messages
            max_queue=10,
            # timeout  defines the maximum wait time in seconds for completing the closing handshake
            timeout=4,
        )
        while self.is_running:
            self.ws = asyncio.Future()
            log.debug('connecting')
            ws = await retry(
                lambda: websockets.connect(self.endpoint, **connection_opts),
                retry_duration=0.75  # second
            )
            log.debug('connected')
            self.ws.set_result(ws)
            receiver = asyncio.ensure_future(self._message_receiver(ws), loop=self.loop)
            if not started.done():
                started.set_result(True)
            await self._connection_did_connect()
            try:
                await asyncio.wait([receiver], loop=self.loop)
            except (websockets.ConnectionClosed, ConnectionAbortedError):
                log.debug('connection lost')
                pass
            self.ws = asyncio.Future()
            await asyncio.ensure_future(self._close_ws(ws), loop=self.loop)
            log.debug('closed connection')
            await self._connection_did_close()

    async def _close_ws(self, ws):
        try:
            await ws.close()
        except:
            log.exception('error while closing connection')

    async def __aenter__(self):
        self.is_running = True
        started = asyncio.Future()
        self.stopped = asyncio.Future()
        self.io_loop = asyncio.ensure_future(self._run_io_loop(started))
        await started
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        log.debug('awaiting completion')
        try:
            await asyncio.wait([self.stopped, self.io_loop], return_when=asyncio.FIRST_COMPLETED)
        except KeyboardInterrupt:
            raise
        log.debug('received completion')


def run_async(coro_or_future):
    try:
        if hasattr(asyncio, 'run'):
            return asyncio.run(coro_or_future)
        else:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(coro_or_future)
    except KeyboardInterrupt:
        pass


__all__ = [
    'DrivelineClient',
    'ClientException',
    'ListResult',
    'Record',
    'Stream',
    'Query',
    'run_async',
]
