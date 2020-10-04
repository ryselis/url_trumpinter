# Create your views here.
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.generic import FormView

from shortener.forms import UrlShortenerForm
from shortener.models import ShortenedUrl


class IndexView(FormView):
    template_name = 'index.html'
    form_class = UrlShortenerForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return {
            **context_data,
            'title': _('Make your URLs short!')
        }

    @transaction.atomic
    def form_valid(self, form):
        created_instance = form.save(commit=True)
        host = self.request.META['HTTP_HOST']
        scheme = 'https' if self.request.is_secure() else "http"
        extra_context = {
            'generated_url': f'{scheme}://{host}/{created_instance.shortened_url_path}/'
        }
        return self.render_to_response(self.get_context_data(**extra_context))


@cache_page(60 * 10)
def get_url_redirect(request, short_url):
    shortened_url = get_object_or_404(ShortenedUrl, shortened_url_path=short_url)
    return HttpResponseRedirect(shortened_url.url)
