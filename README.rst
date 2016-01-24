.. image:: https://travis-ci.org/agile4you/bottle-cache.svg?branch=master
    :target: https://travis-ci.org/agile4you/bottle-cache

.. image:: https://coveralls.io/repos/agile4you/bottle-cache/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/agile4you/bottle-cache?branch=master

**bottle_cache**:  *Cache plugin for bottle.py applications*


*Example Usage*

.. code:: python

    import bottle
    from bottle_cache.plugin import (cache_for, CachePlugin)

    cache = CachePlugin('url_cache', 'redis', host='localhost', port=6379, db=1)

    app = bottle.Bottle()
    app.install(cache)


    # You can either cache the result of a web handler
    # for a ttl (json, or html)

    @app.get('/')
    @cache_for(20, cache_key_func='full_path')
    def api_handler():
        print('Cache miss')
        return {'a': 1, 'b': 3}


    # Or you can inject the cache instance directly
    # to handler for more flexibility and custom implementations

    @app.get('/cache')
    def cache_handler(url_cache):
        return {"cache_info": str(url_cache)}


    bottle.run(app=app, port=8080, reloader=True)