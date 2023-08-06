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

class StreamIdFactory(object):
    __slots__ = ['aliases', 'count', 'free_aliases', 'stream_ids']

    def __init__(self, count: int):
        assert count > 0
        self.stream_ids = list(range(count, -1, -1))
        self.count = count
        self.free_aliases = count
        self.aliases = dict()

    def next(self, stream_name: str):
        if self.free_aliases == 0:
            return stream_name, False
        stream_id = self.stream_ids[self.free_aliases]
        self.free_aliases -= 1
        self.aliases[stream_id] = stream_name
        return stream_id, True

    def release(self, stream_id):
        if isinstance(stream_id, str):
            return
        del self.aliases[stream_id]
        self.free_aliases += 1
        self.stream_ids[self.free_aliases] = stream_id


__all__ = [
    'StreamIdFactory',
]
