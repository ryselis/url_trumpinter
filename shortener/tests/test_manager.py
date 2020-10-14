from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, override_settings

from shortener.models import ShortenedUrl

TEST_CACHE_SETTINGS = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}


class ManagerTestCaseNoURLExists(TestCase):
    @override_settings(CACHES=TEST_CACHE_SETTINGS)
    def test_no_url_exists(self):
        self.assertRaises(ObjectDoesNotExist, ShortenedUrl.objects.get_full_url, 'non-existing-entry')


class ManagerTestCaseURLNotCached(TestCase):
    def setUp(self):
        super().setUp()
        ShortenedUrl.objects.create(shortened_url_path='short-url', url='http://google.com')

    @override_settings(CACHES=TEST_CACHE_SETTINGS)
    def test_url_fetched_from_database(self):
        self.assertNumQueries(1, ShortenedUrl.objects.get_full_url, 'short-url')

    @override_settings(CACHES=TEST_CACHE_SETTINGS)
    def test_correct_url_fetched(self):
        self.assertEquals(ShortenedUrl.objects.get_full_url('short-url'), 'http://google.com')

    def tearDown(self):
        super().tearDown()
        ShortenedUrl.objects.all().delete()
        cache.clear()


class ManagerTestCaseURLCached(TestCase):
    def setUp(self):
        super().setUp()
        ShortenedUrl.objects.create(shortened_url_path='short-url', url='http://google.com')
        cache.set('url_cache_short-url', 'http://google.com')

    @override_settings(CACHES=TEST_CACHE_SETTINGS)
    def test_url_fetched_from_database(self):
        self.assertNumQueries(0, ShortenedUrl.objects.get_full_url, 'short-url')

    @override_settings(CACHES=TEST_CACHE_SETTINGS)
    def test_correct_url_fetched(self):
        self.assertEquals(ShortenedUrl.objects.get_full_url('short-url'), 'http://google.com')

    def tearDown(self):
        ShortenedUrl.objects.all().delete()
        cache.clear()
