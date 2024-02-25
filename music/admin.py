from django.contrib import admin
from import_export.admin import ImportExportMixin
from main.admin import BaseAdmin
from music.forms import *
from music.import_export import *
from django.utils.html import format_html
import main.settings


@admin.register(MusicGenre)
class MusicGenreAdmin(ImportExportMixin, BaseAdmin):
    form = MusicGenreAdminForm
    list_display = ('id', 'name',)
    model = MusicGenre
    ordering = ['id']
    resource_class = MusicGenreResource
    search_fields = ('name',)


class MusicDetailAdmin(admin.TabularInline):
    exclude = BaseAdmin.exclude
    extra = 0
    form = MusicDetailAdminForm
    model = MusicDetail


@admin.register(Music)
class MusicAdmin(ImportExportMixin, BaseAdmin):
    exclude = BaseAdmin.exclude
    form = MusicAdminForm
    inlines = [MusicDetailAdmin]
    list_display = (
        'display_image',
        'title_and_bands',
        'launch_date',
        'album',
        'band',
    )
    list_filter = ('music_genre',)
    list_per_page = 5
    model = Music
    resource_class = MusicResource
    search_fields = (
        'title',
        'album',
        'band',
        'music_genre__name'
    )

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 150px;" />',
                main.settings.BASE_URL + obj.image.url
            )
        else:
            return ''
    display_image.short_description = 'Image'

    def title_and_bands(self, obj):
        edit_url = reverse(
            'admin:music_music_change',
            args=[obj.id]
        )
        return format_html(
            '<a href="{}">{}</a>',
            edit_url, f"{obj.title} | {obj.band}"
        )
    title_and_bands.short_description = 'Title and Band'
