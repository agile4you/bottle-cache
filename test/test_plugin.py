# -*- coding: utf-8 -*-
"""Unit tests for `bottle_cache.plugin` module.
"""

from bottle_cache.plugin import cache_for, CacheInfo


def test_cache_for_deco():
    """Testing bottle_cache.plugin.cache_for decorator.
    """
    @cache_for(20)
    def mock_handler():
        pass

    assert mock_handler.cache_info == CacheInfo(20, 'full_path', 'application/json')
