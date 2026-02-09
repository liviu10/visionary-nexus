from django import forms
from settings.models import *


class CurrencyAdminForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = '__all__'
        widgets = {
            'country': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'currency': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'code': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }


class LanguageAdminForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'code': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }
