# -*- coding: utf-8 -*-
"""Example `bottle_cache` application
"""

import bottle
from bottle_cache.plugin import (cache_for, CachePlugin)

cache = CachePlugin('url_cache', 'redis', host='localhost', port=6379, db=1)

app = bottle.Bottle()
app.install(cache)


@app.get('/')
@cache_for(20, cache_key_func='full_path')
def api_handler():
    return {'a': 1, 'b': 3}

bottle.run(app=app, port=9182, reloader=True)
