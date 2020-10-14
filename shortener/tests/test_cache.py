from django.core.cache import cache
from django.test import TestCase, override_settings

from shortener.cache import set_full_url_to_cache, get_full_url_from_cache


class CacheTestCase(TestCase):
    TEST_CACHE_SETTINGS = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

    @override_settings(CACHES=TEST_CACHE_SETTINGS)
    def test_set_url_exists_in_cache(self):
        set_full_url_to_cache('test_url', 'test_full_url')
        self.assertEquals(cache.get('url_cache_test_url'), 'test_full_url')

    @override_settings(CACHES=TEST_CACHE_SETTINGS)
    def test_url_set_to_cache(self):
        cache.set('url_cache_test_url', 'test_full_url')
        self.assertEquals(get_full_url_from_cache('test_url'), 'test_full_url')

    def tearDown(self):
        super().tearDown()
        cache.delete('url_cache_test_url')
