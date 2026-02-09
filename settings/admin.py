from django.contrib import admin
from import_export.admin import ImportExportMixin
from main.admin import BaseAdmin
from settings.forms import *
from settings.import_export import *


@admin.register(Currency)
class CurrencyAdmin(ImportExportMixin, BaseAdmin):
    form = CurrencyAdminForm
    list_display = ('id', 'country', 'currency', 'code',)
    model = Currency
    ordering = ['id']
    resource_class = CurrencyResource
    search_fields = ('country', 'currency', 'code',)


@admin.register(Language)
class BookLanguageAdmin(ImportExportMixin, BaseAdmin):
    form = LanguageAdminForm
    list_display = ('id', 'name', 'code',)
    model = Language
    ordering = ['id']
    resource_class = LanguageResource
    search_fields = ('name', 'code',)
