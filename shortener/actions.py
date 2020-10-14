from django.contrib import messages
from django.utils.translation import ugettext_lazy as _, ngettext_lazy


def deactivate_short_urls(model_admin, request, queryset):
    """
    Deactivates the selected URLs if they are all active, otherwise the user may be doing something wrong
    """
    if queryset.filter(active=False).exists():  # already deactivated
        messages.error(request, _('Some of the selected URLs have already been deactivated.'))
    else:
        # deactivate; using update does one query, but does not call post_save/pre_save signals. We go for performance here
        updated_urls = queryset.update(active=False)
        messages.success(request, ngettext_lazy('Selected URL has been deactivated.', 'Selected URLs have been deactivated.', number=updated_urls))


deactivate_short_urls.short_description = _('Deactivate')
