# -*- coding: utf-8 -*-
"""`bottle_cache.plugin` module.

Provides bottle.py cache plugin.
"""

from __future__ import absolute_import

__author__ = 'Papavassiliou Vassilis'
__date__ = '23-1-2016'


import bottle
import collections
import ujson


CacheInfo = collections.namedtuple('CacheInfo', 'ttl, cache_key_func, content_type')


def available_backend():
    """Auto loading available cache backend implementation
    without hard-coding them.
    """

    import bottle_cache.backend as backend_module

    available_list = [
        callback for callback in dir(backend_module)
        if 'cachebackend' in callback.lower() and
        'base' not in callback.lower()
    ]

    return {callback.lower().replace('cachebackend', ''): getattr(backend_module, callback)
            for callback in available_list}


def cache_for(ttl, cache_key_func, content_type='application/json'):
    """A decorator that signs a callable object with a 'CacheInfo'
    attribute.

    Args:
        ttl (int): Cache Time to live in seconds.
        content_type (str): Handler response type.
    Returns:
        The callable object.
    """

    def _wrapped(callback):
        setattr(
            callback,
            'cache_info',
            CacheInfo(ttl, cache_key_func, content_type)
        )

        return callback

    return _wrapped


class CachePlugin(object):
    """A `bottle.Bottle` application plugin for `bottle_cache.backend` implementations.

    Attributes:
        keyword (str): The string keyword for application registry.
        provider (instance): A JWTProvider instance.
        login_enable (bool): If True app is mounted with a login handler.
        auth_endpoint (str): The authentication uri for provider if
                             login_enabled is True.
        kwargs : JWTProvider init parameters.
    """

    api = 2

    content_types = (
        ('text/html', lambda x: x),
        ('application/json', ujson.dumps)
    )

    cache_key_rules = {
        'full_path': lambda req, cxt: str(cxt.rule) + req.query_string,
        'query_path': lambda req, cxt: req.query_string,
    }

    def __init__(self, keyword, backend, **backend_kwargs):

        if backend not in available_backend():
            raise bottle.PluginError(
                'Invalid backend {} provided. Available until now: ({})'.format(
                    backend, ', '.join(available_backend().keys())
                )
            )

        self.backend = available_backend()[backend](**backend_kwargs)
        self.keyword = keyword

    def register_rule(self, rule_key, rule_callback):
        self.cache_key_rules[rule_key] = rule_callback
        return self

    def __repr__(self):
        return "<{} instance at: 0x{:x}>".format(self.__class__, id(self))

    def __str__(self):
        return '<{} instance> {}'.format(
            self.__class__.__name__,
            self.keyword
        )

    def __contains__(self, item):
        return item in self.cache_key_rules

    def __getitem__(self, item):
        return self.cache_key_rules.get(item, None)

    def __delitem__(self, key):
        del self.cache_key_rules[key]

    def setup(self, app):  # pragma: no cover
        """Make sure that other installed plugins don't affect the same
        keyword argument and check if metadata is available.
        """
        for other in app.plugins:
            if not isinstance(other, CachePlugin):
                continue
            if other.keyword == self.keyword:
                raise bottle.PluginError(
                    "Found another cache plugin "
                    "with conflicting settings ("
                    "non-unique keyword)."
                )

    def apply(self, callback, context):  # pragma: no cover
        """Implement bottle.py API version 2 `apply` method.
        """
        cache_enabled = getattr(callback, 'cache_info', None)

        if not cache_enabled:
            return callback

        if cache_enabled.cache_key_func not in self:
            raise bottle.PluginError(
                'Unregistered cache key function: '
                '{}.'.format(cache_enabled.cache_key_func)
            )

        def wrapper(*args, **kwargs):

            cache_key_fn = self.cache_key_rules[cache_enabled.cache_key_func]
            key = cache_key_fn(bottle.request, context)
            data = self.backend.get(key)

            if data:
                bottle.response.content_type = cache_enabled.content_type
                return ujson.loads(data)

            result = callback(*args, **kwargs)

            self.backend.set(key, ujson.dumps(result), cache_enabled.ttl)
            return result

        return wrapper
