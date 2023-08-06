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
from concurrent.futures import ThreadPoolExecutor

from .exceptions import ClientException
from .opts import *
from .record_data import *

log = logging.getLogger('driveline')


class Consumer(object):
    __slots__ = ['_client', 'consumer_id', 'options']

    def __init__(self, client, consumer_id):
        self._client = client
        self.consumer_id = consumer_id
        self.options = {}

    @property
    def client(self):
        return self._client

    async def on_reconnect(self):
        return False

    async def on_disconnect(self):
        return False

    def _build_data_records(self, records, tags):
        log.debug('processing tags: %s for %d record (s)', tags, len(records))
        tags = iter(tags or [])
        record_ids = []
        try:
            while True:
                key = next(tags)
                value = next(tags)
                if key == TAG_ID:
                    record_ids = value
        except StopIteration:
            pass
        if len(record_ids) == 0:
            record_ids = [None for _ in range(len(records))]
        else:
            log.debug('got record_ids: %s', record_ids)

        for record, record_id in zip(records, record_ids):
            yield DataRecord(record, record_id)

    async def on_message(self, records=None, tags=None, error=None):
        raise NotImplemented()


class LoadConsumer(Consumer):
    __slots__ = ['key', 'promise']

    def __init__(self, client, consumer_id, key, **options):
        super().__init__(client, consumer_id)
        self._set_read_options(**options)
        self.key = key
        self.promise = asyncio.Future()

    def _set_read_options(self, from_record_id=None):
        self.options.update(from_record_id=from_record_id)

    def result(self):
        return self.promise

    async def on_disconnect(self):
        return True

    async def on_reconnect(self):
        await self.client._load(self)
        return True

    async def on_message(self, records=None, tags=None, error=None):
        log.debug('received load response w/ %d record(s)', len(records))
        if error is not None:
            log.error('something went wrong, resolving error')
            self.promise.set_exception(ClientException(error))
            return False
        for payload in self._build_data_records(records, tags):
            log.debug('resolving the future with %s', payload)
            self.promise.set_result(payload)
            break
        log.debug('resolved future')
        return False


class ListResult(object):
    __slots__ = ['queue']

    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    def __aiter__(self):
        return self

    async def __anext__(self):
        name, error = await self.queue.get()
        if error is not None:
            raise error
        if name is None:
            raise StopAsyncIteration
        return name


class ListConsumer(Consumer):
    __slots__ = ['pattern', 'queue']

    def __init__(self, client, consumer_id, pattern, **options):
        super().__init__(client, consumer_id)
        assert pattern is not None and len(pattern) > 0
        self.pattern = pattern
        self.queue = asyncio.Queue()
        self._set_list_options(**options)

    def _set_list_options(self, **options):
        if len(options) > 0:
            log.warning('ignoring list options %s', options)

    def result(self):
        return ListResult(self.queue)

    async def on_disconnect(self):
        await self.queue.put((None, ClientException('connection lost')))
        return False

    async def on_message(self, records=None, tags=None, error=None):
        log.debug('received list data')
        if error is not None:
            await self.queue.put((None, ClientException(error)))
            return False

        records = cbor.loads(records[0])
        if len(records) == 0:
            log.debug('list data is empty. done receiving results')
            await self.queue.put((None, None))
            return False

        for m in records:
            await self.queue.put((m, None))

        return True


class Query(Consumer):
    __slots__ = ['dql', 'executor', 'handler', 'last_record_id', 'is_continuous', 'options']

    def __init__(self, client, consumer_id: int, dql: str, is_continuous: bool, handler,
                 executor=None,
                 max_concurrency=None,
                 **options):
        super().__init__(client, consumer_id)
        self._set_query_options(**options)
        assert len(dql) > 10 and handler is not None and max_concurrency > 0
        self.dql = dql
        self.is_continuous = is_continuous
        self.handler = handler
        self.executor = executor
        if self.executor is not None:
            self.executor = ThreadPoolExecutor(max_workers=int(max_concurrency))
        self.last_record_id = None

    def _set_query_options(self, from_record_id=None):
        self.options.update(from_record_id=from_record_id)

    @property
    def client(self):
        return self._client.sync_proxy()

    async def on_disconnect(self):
        return self.is_continuous

    async def on_reconnect(self):
        self.options.update(from_record_id=self.last_record_id)
        await self.client._query(self)
        return True

    def result(self):
        return self

    async def on_message(self, records=None, tags=None, error=None):
        if error is not None:
            await self.client.loop.run_in_executor(self.executor, self.handler, ErrorRecord(error))
            return False

        if not self.is_continuous and len(records) == 0:
            # stop condition for quick queries
            try:
                self.handler(None)
            except KeyboardInterrupt:
                raise
            except Exception:
                log.exception('error processing message')
            return False

        log.debug('received %d messages for query %s', len(records), self.dql)
        for m in self._build_data_records(records, tags):
            if (m.record_id or b'') < (self.last_record_id or b''):
                continue
            try:
                await self.client.loop.run_in_executor(self.executor, self.handler, m)
                self.last_record_id = m.record_id
            except KeyboardInterrupt:
                raise
            except Exception:
                log.exception('error processing message')
        return True


class SyncConsumer(Consumer):
    __slots__ = ['promise']

    def __init__(self, client, consumer_id):
        super().__init__(client, consumer_id)
        self.promise = asyncio.Future()

    def result(self):
        return self.promise

    async def on_disconnect(self):
        self.promise.set_exception(ClientException('connection lost'))
        return False

    async def on_reconnect(self):
        return False

    async def on_message(self, records=None, tags=None, error=None):
        log.debug('received load response w/ %d record(s)', len(records))
        if error is not None:
            self.promise.set_exception(ClientException(error))
            return False
        self.promise.set_result(None)
        return False


__all__ = [
    'Query',
    'Consumer',
    'LoadConsumer',
    'ListConsumer',
    'SyncConsumer',
    'ListResult',
]
