from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from entertainment.models import *
from django.utils.safestring import mark_safe
from django.urls import reverse


class EntertainmentConfigAdminForm(forms.ModelForm):
    class Meta:
        model = EntertainmentConfig
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'related_field': forms.Select(attrs={'style': 'width: 100%;'})
        }


class BookImagePreviewWidget(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        if value and hasattr(value, 'url'):
            image_url = value.url
            view_image_url = reverse(
                'admin:entertainment_book_change',
                args=[value.instance.pk]
            )
            output += f'<br/><a href="{image_url}" target="_blank">View Image</a>'
        return mark_safe(output)


class BookAdminForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'book_type': forms.Select(attrs={'style': 'width: 100%;'}),
            'book_language': forms.Select(attrs={'style': 'width: 100%;'}),
            'authors': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'image': BookImagePreviewWidget(attrs={'style': 'width: 100%;'}),
            'title': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'book_genre': forms.Select(attrs={'style': 'width: 100%;'}),
            'rating': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'published_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 100%;'}),
            'description': CKEditor5Widget(attrs={'style': 'width: 100%'}, config_name="extends"),
            'isbn_13': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'page_count': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'book_status': forms.Select(attrs={'style': 'width: 100%;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        book_types_choices = EntertainmentConfig.objects.filter(related_field='book_types')
        self.fields['book_type'].queryset = book_types_choices

        book_languages_choices = EntertainmentConfig.objects.filter(related_field='book_languages')
        self.fields['book_language'].queryset = book_languages_choices

        book_genres_choices = EntertainmentConfig.objects.filter(related_field='book_genres')
        self.fields['book_genre'].queryset = book_genres_choices

        self.fields['description'].required = False

        book_status_choices = EntertainmentConfig.objects.filter(related_field='book_statuses')
        self.fields['book_status'].queryset = book_status_choices


class BookDetailAdminForm(forms.ModelForm):
    class Meta:
        model = BookDetail
        fields = '__all__'
        widgets = {
            'buy_link': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'download_link': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'amount': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'book_detail_currency': forms.Select(attrs={'style': 'width: auto;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        book_detail_currencies = EntertainmentConfig.objects.filter(related_field='book_detail_currencies')
        self.fields['book_detail_currency'].queryset = book_detail_currencies


class GameImagePreviewWidget(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        if value and hasattr(value, 'url'):
            image_url = value.url
            view_image_url = reverse(
                'admin:entertainment_book_change',
                args=[value.instance.pk]
            )
            output += f'<br/><a href="{image_url}" target="_blank">View Image</a>'
        return mark_safe(output)


class GameAdminForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'
        widgets = {
            'image': GameImagePreviewWidget(attrs={'style': 'width: 100%;'}),
            'title': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'game_genre': forms.Select(attrs={'style': 'width: 100%;'}),
            'rating': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'released_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 100%;'}),
            'description': CKEditor5Widget(attrs={'style': 'width: 100%'}, config_name="extends"),
            'game_status': forms.Select(attrs={'style': 'width: 100%;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        game_genres_choices = EntertainmentConfig.objects.filter(related_field='game_genres')
        self.fields['game_genre'].queryset = game_genres_choices

        self.fields['description'].required = False

        game_statuses_choices = EntertainmentConfig.objects.filter(related_field='game_statuses')
        self.fields['game_status'].queryset = game_statuses_choices


class GameDetailAdminForm(forms.ModelForm):
    class Meta:
        model = GameDetail
        fields = '__all__'
        widgets = {
            'buy_link': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'download_link': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'amount': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'game_detail_currency': forms.Select(attrs={'style': 'width: auto;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        game_detail_currencies = EntertainmentConfig.objects.filter(related_field='game_detail_currencies')
        self.fields['game_detail_currency'].queryset = game_detail_currencies


class MediaImagePreviewWidget(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        if value and hasattr(value, 'url'):
            image_url = value.url
            view_image_url = reverse(
                'admin:entertainment_book_change',
                args=[value.instance.pk]
            )
            output += f'<br/><a href="{image_url}" target="_blank">View Image</a>'
        return mark_safe(output)


class MediaAdminForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = '__all__'
        widgets = {
            'media_type': forms.Select(attrs={'style': 'width: 100%;'}),
            'image': MediaImagePreviewWidget(attrs={'style': 'width: 100%;'}),
            'title': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'original_title': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'media_genre': forms.Select(attrs={'style': 'width: 100%;'}),
            'rating': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'launch_date': forms.DateInput(attrs={'type': 'date', 'style': 'width: 100%;'}),
            'description': CKEditor5Widget(attrs={'style': 'width: 100%'}, config_name="extends"),
            'imdb_link': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'media_status': forms.Select(attrs={'style': 'width: 100%;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        media_types_choices = EntertainmentConfig.objects.filter(related_field='media_types')
        self.fields['media_type'].queryset = media_types_choices

        media_genres_choices = EntertainmentConfig.objects.filter(related_field='media_genres')
        self.fields['media_genre'].queryset = media_genres_choices

        self.fields['description'].required = False

        media_status_choices = EntertainmentConfig.objects.filter(related_field='media_statuses')
        self.fields['media_status'].queryset = media_status_choices


class MediaDetailAdminForm(forms.ModelForm):
    class Meta:
        model = MediaDetail
        fields = '__all__'
        widgets = {
            'amount': forms.TextInput(attrs={'style': 'width: 98%; margin-right: 4px;'}),
            'download_link': forms.TextInput(attrs={'style': 'width: 98%;'}),
        }
