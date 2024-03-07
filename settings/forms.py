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


class LogTypeAdminForm(forms.ModelForm):
    class Meta:
        model = LogType
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'description': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'when': forms.TextInput(attrs={'style': 'width: 100%;'}),
        }


class LogEventAdminForm(forms.ModelForm):
    class Meta:
        model = LogEvent
        fields = '__all__'
        widgets = {
            'log_type': forms.Select(attrs={'style': 'width: 100%;'}),
            'description': forms.TextInput(attrs={'style': 'width: 100%;'}),
            'request_details': forms.Textarea(attrs={'style': 'width: 100%; resize: none'}),
            'response_details': forms.Textarea(attrs={'style': 'width: 100%; resize: none'}),
            'sql_details': forms.Textarea(attrs={'style': 'width: 100%; resize: none'}),
        }
