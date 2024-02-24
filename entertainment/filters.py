from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from entertainment.models import *


class BookGenreFilter(admin.SimpleListFilter):
    parameter_name = 'book_genre'
    related_field = 'book_genres'
    lookup_field = 'book_genre'
    queryset_field = 'book_genre'
    title = _('genre')

    def lookups(self, request, model_admin):
        return EntertainmentConfig.objects.filter(related_field=self.related_field).values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            filter_args = {f'{self.queryset_field}__id': self.value()}
            return queryset.filter(**filter_args)
        return queryset


class BookTypeFilter(admin.SimpleListFilter):
    parameter_name = 'book_type'
    related_field = 'book_types'
    lookup_field = 'book_type'
    queryset_field = 'book_type'
    title = _('type')

    def lookups(self, request, model_admin):
        return EntertainmentConfig.objects.filter(related_field=self.related_field).values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            filter_args = {f'{self.queryset_field}__id': self.value()}
            return queryset.filter(**filter_args)
        return queryset


class BookStatusFilter(admin.SimpleListFilter):
    parameter_name = 'book_status'
    related_field = 'book_statuses'
    lookup_field = 'book_status'
    queryset_field = 'book_status'
    title = _('status')

    def lookups(self, request, model_admin):
        return EntertainmentConfig.objects.filter(related_field=self.related_field).values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            filter_args = {f'{self.queryset_field}__id': self.value()}
            return queryset.filter(**filter_args)
        return queryset


class GameStatusFilter(admin.SimpleListFilter):
    parameter_name = 'game_status'
    related_field = 'game_statuses'
    lookup_field = 'game_status'
    queryset_field = 'game_status'
    title = _('status')

    def lookups(self, request, model_admin):
        return EntertainmentConfig.objects.filter(related_field=self.related_field).values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            filter_args = {f'{self.queryset_field}__id': self.value()}
            return queryset.filter(**filter_args)
        return queryset


class GameGenreFilter(admin.SimpleListFilter):
    parameter_name = 'game_genre'
    related_field = 'game_genres'
    lookup_field = 'game_genre'
    queryset_field = 'game_genre'
    title = _('genre')

    def lookups(self, request, model_admin):
        return EntertainmentConfig.objects.filter(related_field=self.related_field).values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            filter_args = {f'{self.queryset_field}__id': self.value()}
            return queryset.filter(**filter_args)
        return queryset


class MediaTypeFilter(admin.SimpleListFilter):
    parameter_name = 'media_type'
    related_field = 'media_types'
    lookup_field = 'media_type'
    queryset_field = 'media_type'
    title = _('type')

    def lookups(self, request, model_admin):
        return EntertainmentConfig.objects.filter(related_field=self.related_field).values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            filter_args = {f'{self.queryset_field}__id': self.value()}
            return queryset.filter(**filter_args)
        return queryset


class MediaGenreFilter(admin.SimpleListFilter):
    parameter_name = 'media_genre'
    related_field = 'media_genres'
    lookup_field = 'media_genre'
    queryset_field = 'media_genre'
    title = _('genre')

    def lookups(self, request, model_admin):
        return EntertainmentConfig.objects.filter(related_field=self.related_field).values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            filter_args = {f'{self.queryset_field}__id': self.value()}
            return queryset.filter(**filter_args)
        return queryset


class MediaStatusFilter(admin.SimpleListFilter):
    parameter_name = 'media_status'
    related_field = 'media_statuses'
    lookup_field = 'media_status'
    queryset_field = 'media_status'
    title = _('status')

    def lookups(self, request, model_admin):
        return EntertainmentConfig.objects.filter(related_field=self.related_field).values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            filter_args = {f'{self.queryset_field}__id': self.value()}
            return queryset.filter(**filter_args)
        return queryset
