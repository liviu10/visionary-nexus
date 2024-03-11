from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from games.models import *
from django.utils.safestring import mark_safe
from django.urls import reverse


class GameGenreAdminForm(forms.ModelForm):
    class Meta:
        model = GameGenre
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }


class GameStatusAdminForm(forms.ModelForm):
    class Meta:
        model = GameStatus
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }


class GameImagePreviewWidget(forms.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        if value and hasattr(value, 'url'):
            image_url = value.url
            view_image_url = reverse(
                'admin:games_game_change',
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
            'game_link': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'game_image_link': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False


class GameDetailAdminForm(forms.ModelForm):
    class Meta:
        model = GameDetail
        fields = '__all__'
        widgets = {
            'buy_link': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'download_link': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'amount': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'game_currency': forms.Select(attrs={'style': 'width: auto;'}),
        }
