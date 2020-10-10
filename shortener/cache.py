from typing import Optional

from django.core.cache import cache


CACHE_TIMEOUT = 3600  # in seconds; configures the expiry of a URL in cache


def get_full_url_from_cache(short_url: str) -> Optional[str]:
    """
    Gets a given shortened URL's corresponding full url if it exists in cache
    :param short_url: a short URL that may exist in cache
    :return: full URL if it's cached, None otherwise
    """
    cache_key = _get_cache_key(short_url)
    return cache.get(cache_key)


def set_full_url_to_cache(short_url: str, full_url: str):
    """
    Sets a cache entry for a URL
    :param short_url:
    :param full_url:
    :return:
    """
    cache_key = _get_cache_key(short_url)
    cache.set(cache_key, full_url, CACHE_TIMEOUT)


def _get_cache_key(short_url: str) -> str:
    return f'url_cache_{short_url}'
