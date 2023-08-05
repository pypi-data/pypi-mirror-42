# -*- coding: utf-8 -*-

import time
from functools import partial

# tests only
_SKIP_CACHE = False


class cache:
    """A decorator for a simple in memory cache.

    Usage:
    ^^^^^^

    @cache(10)  # a 10 seconds cache.
    def my_func():
        return 10**1000
    """

    def __init__(self, cache_time):
        """:param cache_time: How long should we keep the cache in memory."""

        self.cache_time = cache_time
        # So here the key is the return of self._get_cache_key and the
        # value is the time when we got the result
        self.last_call = {}
        # the key is the same as the above and the value is the cached result
        self.last_result = {}

    def _get_cache_key(self, *args, **kwargs):
        k = (str(args), str(kwargs))
        return k

    async def _wrapper(self, fn, *args, **kwargs):

        key = self._get_cache_key(*args, **kwargs)

        last_call = self.last_call.get(key)
        last_result = self.last_result.get(key)
        now = time.time()

        if last_call and (last_call + self.cache_time) > now \
           and not _SKIP_CACHE:
            return last_result

        last_result = await fn(*args, **kwargs)
        self.last_result[key] = last_result
        self.last_call[key] = time.time()
        return last_result

    def __call__(self, fn):
        wrapper = partial(self._wrapper, fn)
        return wrapper
