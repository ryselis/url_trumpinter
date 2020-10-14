# Create your views here.
from datetime import datetime

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from shortener.forms import UrlShortenerForm
from shortener.models import ShortenedUrl
from shortener.utils import get_client_ip


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
        # create and save shortened URL
        created_instance = form.save(commit=True)
        # get full generated URL and add it to context
        host = self.request.META['HTTP_HOST']
        scheme = 'https' if self.request.is_secure() else "http"
        extra_context = {
            'generated_url': f'{scheme}://{host}/{created_instance.shortened_url_path}/'
        }
        return self.render_to_response(self.get_context_data(**extra_context))


def get_url_redirect(request, short_url: str):
    """
    Given a short URL, generates an HttpResponseRedirect to a corresponding target URL
    """
    # only allow URLs that have not been deactivated
    url_object = get_object_or_404(ShortenedUrl, Q(expiration_time__isnull=True) | Q(expiration_time__gte=datetime.now()),
                                   shortened_url_path=short_url, active=True)
    url_object.clicks.create(referer=request.META.get('HTTP_REFERER'), ip_address=get_client_ip(request))
    full_url = url_object.url
    return HttpResponseRedirect(full_url)


# there is a couple more optional features to be implemented here and in other places.
# admin interface could be provided by creating an admin class that inherits from Django's ModelAdmin, and providing list_display with required
# columns to be shown in changelist. Deletion would be handled entirely by Django admin; link deactivation could be achieved by adding a boolean
# field to ShortenedUrl model with default value True; an action list would be provided to ShortenedUrl admin, it would contain one action - a
# function that accepts model admin, request and queryset and does ShortenedUrl.objects.update which sets the field value to False.

# click stats may be recorded by adding one more model: ShortenedUrlClick with the fields given in task description plus a FK field to
# ShortenedUrl. An instance of this class would be created each time get_url_redirect finds an object. Admin interface could have an annotation
# that counts all clicks for ShortenedUrls inside admin's get_queryset method and then used in a custom column. Caching would not exactly work
# because we would also need to have a ShortenedUrl's ID, so we either leave just a DB index to handle the performance, add another caching to
# cache URL ids or go googling for more advanced techniques :)

# expiration would be implemented by adding expiration time field to the ShortenedURL model and it would be checked inside get_url_redirect along
# the lines of ShortenedUrl.objects.get(shortened_url_path=short_url, expiration_time__gte=datetime.now()). This would require a better DB index,
# e.g., index_together for shortened_url_path and expiration_time.

# maximum number of clicks is no different from expiration time, the implementation would be the same

# I have no experience with Docker, I could not do this without spending some time learning Docker.

# a benchmark could be done by generating a lot of ShortenedUrls and then trying to fetch them from the database. This is a very complex topic
# though; benchmarks depend on hardware, server setup, DB configuration, concurrent connections, other processes running on the server,
# maybe also on wind direction - benchmarks should not be done by showcasing something, but showing that the created software meets its requirements.

