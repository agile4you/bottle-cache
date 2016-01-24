# -*- coding: utf-8 -*-
"""Unit test fixtures for `bottle-cache` project.
"""

import pytest
from bottle_cache.backend import RedisCacheBackend
import datetime
from collections import namedtuple


@pytest.fixture(scope='session')
def mock_redis():

    redis_value = namedtuple('RedisValue', 'value, ttl, added')

    class RedisMock(object):

        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self._db = {}

        def flushall(self):
            self._db = {}

        def delete(self, key):
            if key in self._db:
                del self._db[key]

        def set(self, key, value):
            self._db[key] = redis_value(str(value), None, None)

        def setex(self, key, ttl, value):
            self._db[key] = redis_value(str(value), ttl, datetime.datetime.utcnow())

        def get(self, key):
            cache_data = self._db.get(key)

            if not cache_data:
                return None

            if not cache_data.ttl:
                return cache_data.value

            if cache_data.added + datetime.timedelta(seconds=cache_data.ttl) > datetime.datetime.utcnow():
                return cache_data.value
            return None

    return RedisMock(db=0, host='localhost', port=6379)


@pytest.fixture(scope='session')
def mock_redis_cache(mock_redis):
    cache = RedisCacheBackend(backend_client=mock_redis.__class__, db=0, port=6379)
    return cache
