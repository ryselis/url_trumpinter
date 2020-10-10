import string
from random import SystemRandom

from django.db import models
from django.utils.translation import ugettext_lazy as _

from shortener.managers import ShortenedUrlManager


class ShortenedUrl(models.Model):
    url = models.URLField(verbose_name=_('URL'))
    shortened_url_path = models.CharField(max_length=8, verbose_name=_('Short URL path'), db_index=True, unique=True)

    objects = ShortenedUrlManager()


def get_shortened_url(url_length):
    def generate_value():
        return ''.join(random_generator.choice(available_characters) for _ in range(url_length))

    random_generator = SystemRandom()
    available_characters = string.ascii_letters + string.digits
    value = generate_value()
    while ShortenedUrl.objects.filter(shortened_url_path=value).exists():
        value = generate_value()
    return value
