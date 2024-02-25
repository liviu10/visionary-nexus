from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from books.models import *
from django.utils.safestring import mark_safe
from django.urls import reverse


class BookTypeAdminForm(forms.ModelForm):
    class Meta:
        model = BookType
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }


class BookLanguageAdminForm(forms.ModelForm):
    class Meta:
        model = BookLanguage
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }


class BookGenreAdminForm(forms.ModelForm):
    class Meta:
        model = BookGenre
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }


class BookStatusAdminForm(forms.ModelForm):
    class Meta:
        model = BookStatus
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }


class BookImagePreviewWidget(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        if value and hasattr(value, 'url'):
            image_url = value.url
            view_image_url = reverse(
                'admin:books_book_change',
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
        self.fields['description'].required = False


class BookDetailAdminForm(forms.ModelForm):
    class Meta:
        model = BookDetail
        fields = '__all__'
        widgets = {
            'buy_link': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'download_link': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'amount': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'book_currency': forms.Select(attrs={'style': 'width: auto;'}),
        }
