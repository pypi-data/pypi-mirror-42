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


class SyncProxy(object):

    def __init__(self, async_target):
        self.async_target = async_target

    def __getattr__(self, item):
        method = getattr(self.async_target, item + '_sync', None)
        if method is not None:
            return method
        return getattr(self.async_target, item)


class AutoSync(object):

    def __getattr__(self, item):
        if not item.endswith('_sync'):
            raise AttributeError(item)

        method = getattr(self, item[:-5], None)
        config = getattr(method, '__auto_sync__', None)
        if config is None:
            raise AttributeError(item)

        sync_method = self._synchronized(method, **config)
        setattr(self, item, sync_method)
        return sync_method

    def _synchronized(self, fn, **_config):
        def wrapper(*args, **kwds):
            return asyncio.run_coroutine_threadsafe(fn(*args, **kwds), loop=self.get_loop()).result()

        return wrapper

    def sync_proxy(self):
        return SyncProxy(self)


def synchronous(**config):
    def decorator(func):
        func.__auto_sync__ = config
        return func

    return decorator


__all__ = [
    'AutoSync',
    'SyncProxy',
    'synchronous',
]
