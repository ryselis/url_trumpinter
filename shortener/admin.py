from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from shortener.actions import deactivate_short_urls
from shortener.models import ShortenedUrl


class ShortenedUrlAdmin(admin.ModelAdmin):
    actions = [deactivate_short_urls]
    list_display = ('url', 'shortened_url_path', 'active', 'get_click_statistics')

    def get_click_statistics(self, obj: ShortenedUrl):
        """
        Get click statistics for the short URL: click count and the latest clicks. Clicks are displayed in a table
        """
        clicks = obj.clicks.all()  # this is fetched in get_queryset
        time_format = '%Y-%m-%d %H:%M'
        if not clicks:
            return ''
        max_clicks_to_show = 10  # clicks are limited because rendering too many rows in a table will kill the browser (and possibly the server)
        stats = format_html_join('', '<tr><td>{}</td><td>{}</td><td>{}</td></tr>',
                                 ((click.time_clicked.strftime(time_format), click.ip_address, click.referer or '-')
                                  for click in clicks[:max_clicks_to_show]))
        return mark_safe(f'<div>{_("Total clicks")}: {len(clicks)}'  # clicks already fetched, so use len instead of clicks.count()
                         f'<table>'
                         f'<tr><th>{_("Time")}</th><th>{_("IP address")}</th><th>{_("Referer")}</th></tr>'
                         f'<tbody>{stats}</tbody>'
                         f'</table>')
    get_click_statistics.short_description = _('Click statistics')

    def get_queryset(self, request):
        # get clicks for all urls in the queryset. We actually use only part of the clicks, not all of them. In case of many clicks it would be
        # more efficient to fetch first X clicks for each url in separate queries, but prefetch is better for low amount of clicks
        return super().get_queryset(request).prefetch_related('clicks')


admin.site.register(ShortenedUrl, ShortenedUrlAdmin)
