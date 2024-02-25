from django import forms
from music.models import *
from django.utils.safestring import mark_safe
from django.urls import reverse


class MusicGenreAdminForm(forms.ModelForm):
    class Meta:
        model = MusicGenre
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }


class MusicImagePreviewWidget(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        if value and hasattr(value, 'url'):
            image_url = value.url
            view_image_url = reverse(
                'admin:music_music_change',
                args=[value.instance.pk]
            )
            output += f'<br/><a href="{image_url}" target="_blank">View Image</a>'
        return mark_safe(output)


class MusicAdminForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = '__all__'
        widgets = {
            'image': MusicImagePreviewWidget(attrs={'style': 'width: 100%;'}),
            'title': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'music_genre': forms.Select(attrs={'style': 'width: 100%;'}),
            'launch_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 100%;'}),
            'album': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'band': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }


class MusicDetailAdminForm(forms.ModelForm):
    class Meta:
        model = MusicDetail
        fields = '__all__'
        widgets = {
            'amount': forms.TextInput(attrs={'style': 'width: 98%; margin-right: 4px;'}),
            'download_link': forms.TextInput(attrs={'style': 'width: 98%;'}),
            'lyrics_link': forms.TextInput(attrs={'style': 'width: 98%;'}),
        }
