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

from .exceptions import ClientException
import cbor


class Record(object):
    @property
    def record(self):
        raise NotImplemented()

    @property
    def raw_record(self):
        raise NotImplemented()

    @property
    def record_id(self):
        raise NotImplemented()


class DataRecord(Record):
    __slots__ = ['_record', '_record_id']

    def __init__(self, record, record_id):
        self._record = record
        self._record_id = record_id

    @property
    def record(self):
        if self._record is None:
            return None
        return cbor.loads(self._record)

    @property
    def raw_record(self):
        return self._record

    @property
    def record_id(self):
        return self._record_id


class ErrorRecord(Record):
    __slots__ = ['error']

    def __init__(self, error):
        self.error = error

    @property
    def record(self):
        raise ClientException(self.error)

    @property
    def raw_record(self):
        raise ClientException(self.error)

    @property
    def record_id(self):
        raise ClientException(self.error)


__all__ = [
    'DataRecord',
    'ErrorRecord',
    'Record',
]
