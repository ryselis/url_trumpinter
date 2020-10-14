from django.template.response import TemplateResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse

from shortener.models import ShortenedUrl
from shortener.views import IndexView


class IndexViewContextTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self._request_factory = RequestFactory()

    def test_title_and_form_in_context(self):
        request = self._request_factory.get(reverse('index'))
        view = IndexView()
        view.setup(request)
        context = view.get_context_data()
        self.assertIn('title', context)
        self.assertIn('form', context)

    def test_url_created_on_valid_data(self):
        request = self._request_factory.post(reverse('index'), data={'url': 'http://google.com'}, HTTP_HOST='localhost')
        view = IndexView()
        view.setup(request)
        view.dispatch(request)
        self.assertEquals(ShortenedUrl.objects.filter(url='http://google.com').count(), 1)

    def test_generated_url_in_view_response(self):
        request = self._request_factory.post(reverse('index'), data={'url': 'http://google.com'}, HTTP_HOST='localhost')
        view = IndexView()
        view.setup(request)
        response = view.dispatch(request)
        self.assertIn('generated_url', response.context_data)

    def tearDown(self):
        super().tearDown()
        ShortenedUrl.objects.all().delete()
