# -*- coding: utf-8 -*-
"""Unit tests for `bottle_cache.backend` module.
"""


import time


def test_redis_mock_set(mock_redis):
    mock_redis.set('name', 'John')
    assert mock_redis.get('name') == 'John'


def test_redis_mock_setex_valid(mock_redis):
    mock_redis.setex('job', 2, 'developer')
    assert mock_redis.get('job') == 'developer'


def test_redis_mock_setex_invalid(mock_redis):
    mock_redis.setex('age', 1, 28)
    time.sleep(1)

    assert mock_redis.get('age') is None


def test_redis_cache_set(mock_redis_cache):
    """Testing 'bottle_cache.backend.RedisCacheBackend.set' method.
    """

    data = {"a": 1, "b": 2, "c": 3}

    mock_redis_cache.set('a', data)

    assert mock_redis_cache.get('a') == str(data)


def test_redis_cache_set_ttl_valid(mock_redis_cache):
    """Testing 'bottle_cache.backend.RedisCacheBackend.set' method with valid ttl.
    """

    data = {"a": 1, "b": 2, "c": 3}

    mock_redis_cache.set('b', data, 10)

    assert mock_redis_cache.get('b') == str(data)


def test_redis_cache_set_ttl_invalid(mock_redis_cache):
    """Testing 'bottle_cache.backend.RedisCacheBackend.set' method with invalid ttl.
    """

    data = {"a": 1, "b": 2, "c": 3}

    mock_redis_cache.set('c', data, 1)

    time.sleep(1)

    assert mock_redis_cache.get('c') is None


def test_redis_cache_remove(mock_redis_cache):
    """Testing 'bottle_cache.backend.RedisCacheBackend.remove' method.
    """

    data = {"a": 1, "b": 2, "c": 3}

    mock_redis_cache.set('d', data)

    assert mock_redis_cache.get('d')

    mock_redis_cache.remove('d')

    assert mock_redis_cache.get('d') is None


def test_redis_cache_clear(mock_redis_cache):
    """Testing 'bottle_cache.backend.RedisCacheBackend.remove' method.
    """

    assert mock_redis_cache.get('a')

    mock_redis_cache.clear()

    assert mock_redis_cache.get('a') is None
