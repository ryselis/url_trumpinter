from django.http import Http404, HttpResponseRedirect
from django.test import TestCase, RequestFactory
from django.urls import reverse

from shortener.models import ShortenedUrl
from shortener.views import get_url_redirect


class UrlRedirectTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self._shortened_url = ShortenedUrl.objects.create(url='http://google.com', shortened_url_path='12345678')
        self._request_factory = RequestFactory()

    def test_non_existing_url_raises_404(self):
        short_url = 'non-existing'
        request = self._request_factory.get(reverse('get_short_url', kwargs={'short_url': short_url}))
        self.assertRaises(Http404, get_url_redirect, request, short_url)

    def test_existing_url_returns_redirect(self):
        short_url = '12345678'
        request = self._request_factory.get(reverse('get_short_url', kwargs={'short_url': short_url}))
        response = get_url_redirect(request, short_url)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['Location'], 'http://google.com')

    def tearDown(self):
        super().tearDown()
        self._shortened_url.delete()
