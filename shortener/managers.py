from django.db.models import QuerySet, Manager

from shortener.cache import get_full_url_from_cache, set_full_url_to_cache


class ShortenedUrlQuerySet(QuerySet):
    def get_full_url(self, short_url: str) -> str:
        """
        Given a short URL, returns a full URL or raises an ObjectDoesNotExist exception. Utilises cache
        :param short_url: a short URL to get a full URL for
        :return: a full URL corresponding to a short URL
        """
        full_url = get_full_url_from_cache(short_url)
        if not full_url:  # not in cache - get from DB and set to cache
            full_url = self.get(shortened_url_path=short_url).url
            set_full_url_to_cache(short_url, full_url)
        return full_url


class ShortenedUrlManager(Manager.from_queryset(ShortenedUrlQuerySet)):
    pass
