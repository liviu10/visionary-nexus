from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from movies.models import *
from django.utils.safestring import mark_safe
from django.urls import reverse


class MovieTypeAdminForm(forms.ModelForm):
    class Meta:
        model = MovieType
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }


class MovieGenreAdminForm(forms.ModelForm):
    class Meta:
        model = MovieGenre
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }


class MovieStatusAdminForm(forms.ModelForm):
    class Meta:
        model = MovieStatus
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }


class MovieImagePreviewWidget(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        if value and hasattr(value, 'url'):
            image_url = value.url
            view_image_url = reverse(
                'admin:movies_movie_change',
                args=[value.instance.pk]
            )
            output += f'<br/><a href="{image_url}" target="_blank">View Image</a>'
        return mark_safe(output)


class MovieAdminForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'
        widgets = {
            'media_type': forms.Select(attrs={'style': 'width: 100%;'}),
            'image': MovieImagePreviewWidget(attrs={'style': 'width: 100%;'}),
            'title': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'original_title': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'movie_genre': forms.Select(attrs={'style': 'width: 100%;'}),
            'rating': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'launch_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 100%;'}),
            'description': CKEditor5Widget(attrs={'style': 'width: 100%'}, config_name="extends"),
            'imdb_link': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'media_status': forms.Select(attrs={'style': 'width: 100%;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False


class MovieDetailAdminForm(forms.ModelForm):
    class Meta:
        model = MovieDetail
        fields = '__all__'
        widgets = {
            'amount': forms.TextInput(attrs={'style': 'width: 98%; margin-right: 4px;'}),
            'download_link': forms.TextInput(attrs={'style': 'width: 98%;'}),
        }
