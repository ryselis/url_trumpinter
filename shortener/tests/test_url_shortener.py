from unittest import mock

from django.test import TestCase

from shortener.models import get_shortened_url, ShortenedUrl


class MockSystemRandom:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._call_count = 0

    def choice(self, iterable):
        res = iterable[self._call_count % len(iterable)]
        self._call_count = (self._call_count + 1) % len(iterable)
        return res


class UrlShortenerTestCase(TestCase):
    @mock.patch('shortener.models.SystemRandom', MockSystemRandom)
    def test_random_url_generated(self):
        shortened = get_shortened_url(8)
        self.assertEquals(shortened, 'abcdefgh')


class UrlShortenerEntriesExistTestCase(TestCase):
    def setUp(self):
        super().setUp()
        ShortenedUrl.objects.create(url='http://google.com', shortened_url_path='abcdefgh')

    @mock.patch('shortener.models.SystemRandom', MockSystemRandom)
    def test_random_url_generated(self):
        shortened = get_shortened_url(8)
        self.assertEquals(shortened, 'ijklmnop')

    def tearDown(self):
        super().tearDown()
        ShortenedUrl.objects.all().delete()
