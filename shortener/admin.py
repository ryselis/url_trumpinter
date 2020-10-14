from django.contrib import admin

from shortener.actions import deactivate_short_urls
from shortener.models import ShortenedUrl


class ShortenedUrlAdmin(admin.ModelAdmin):
    actions = [deactivate_short_urls]
    list_display = ('url', 'shortened_url_path', 'active')


admin.site.register(ShortenedUrl, ShortenedUrlAdmin)
