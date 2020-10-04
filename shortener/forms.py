from django import forms

from shortener.models import ShortenedUrl, get_shortened_url


class UrlShortenerForm(forms.ModelForm):
    class Meta:
        model = ShortenedUrl
        fields = ('url',)

    def save(self, commit=True):
        shortened_url = super().save(commit=False)
        shortened_url.shortened_url_path = get_shortened_url(url_length=8)
        if commit:
            shortened_url.save()
        return shortened_url
