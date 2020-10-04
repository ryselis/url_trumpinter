from django.urls import path

from shortener.views import IndexView, get_url_redirect

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<short_url>/', get_url_redirect, name='get_short_url')
]