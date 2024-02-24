from django.contrib import admin
from entertainment.models import *
from import_export.admin import ImportExportMixin
from main.admin import BaseAdmin
from entertainment.forms import *
from entertainment.import_export import *
from entertainment.filters import *
from django.utils.html import format_html
import main.settings


@admin.register(EntertainmentConfig)
class EntertainmentConfigAdmin(ImportExportMixin, BaseAdmin):
    form = EntertainmentConfigAdminForm
    list_display = ('id', 'name', 'related_field')
    list_filter = ('related_field',)
    model = EntertainmentConfig
    ordering = ['id']
    resource_class = EntertainmentConfigResource
    search_fields = ('name', 'related_field')


class BookDetailAdmin(admin.TabularInline):
    exclude = BaseAdmin.exclude
    extra = 0
    form = BookDetailAdminForm
    model = BookDetail


@admin.register(Book)
class BookAdmin(ImportExportMixin, BaseAdmin):
    exclude = BaseAdmin.exclude
    form = BookAdminForm
    inlines = [BookDetailAdmin]
    list_display = (
        'display_image',
        'type',
        'title_and_authors',
        'genre',
        'display_rating',
        'published_date',
        'isbn_13',
        'pages',
        'status'
    )
    list_filter = (BookTypeFilter, BookGenreFilter, BookStatusFilter,)
    list_per_page = 5
    model = Book
    resource_class = BookResource
    search_fields = (
        'title',
        'authors',
        'isbn_13',
        'book_genre__name'
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

    def type(self, obj):
        return obj.book_type.name
    type.short_description = 'Type'

    def title_and_authors(self, obj):
        edit_url = reverse(
            'admin:entertainment_book_change',
            args=[obj.id]
        )
        return format_html(
            '<a href="{}">{}</a>',
            edit_url, f"{obj.authors} | {obj.title}"
        )
    title_and_authors.short_description = 'Authors and title'

    def genre(self, obj):
        return obj.book_genre.name
    genre.short_description = 'Genre'

    def display_rating(self, obj):
        rating_stars = '⭐' * int(obj.rating)
        return format_html(
            '<span title="{}"><strong>{}</strong></span> ({})',
            obj.rating, rating_stars, obj.rating
        )
    display_rating.short_description = 'Rating'

    def pages(self, obj):
        return obj.page_count
    pages.short_description = 'Pages'

    def status(self, obj):
        return obj.book_status.name
    status.short_description = 'Status'


class GameDetailAdmin(admin.TabularInline):
    exclude = BaseAdmin.exclude
    extra = 0
    form = GameDetailAdminForm
    model = GameDetail


@admin.register(Game)
class GameAdmin(ImportExportMixin, BaseAdmin):
    exclude = BaseAdmin.exclude
    form = GameAdminForm
    inlines = [GameDetailAdmin]
    list_display = (
        'display_image',
        'title_and_genres',
        'display_rating',
        'released_date',
        'status'
    )
    list_filter = (GameGenreFilter, GameStatusFilter,)
    list_per_page = 5
    model = Game
    resource_class = GameResource
    search_fields = (
        'title',
        'game_genre__name'
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

    def title_and_genres(self, obj):
        edit_url = reverse(
            'admin:entertainment_game_change',
            args=[obj.id]
        )
        return format_html(
            '<a href="{}">{}</a>',
            edit_url, f"{obj.title} | {obj.game_genre.name}"
        )
    title_and_genres.short_description = 'Title and Genre'

    def display_rating(self, obj):
        rating_stars = '⭐' * int(obj.rating)
        return format_html(
            '<span title="{}"><strong>{}</strong></span> ({})',
            obj.rating, rating_stars, obj.rating
        )
    display_rating.short_description = 'Rating'

    def status(self, obj):
        return obj.game_status.name
    status.short_description = 'Status'


class MediaDetailAdmin(admin.TabularInline):
    exclude = BaseAdmin.exclude
    extra = 0
    form = MediaDetailAdminForm
    model = MediaDetail


@admin.register(Media)
class MediaAdmin(ImportExportMixin, BaseAdmin):
    exclude = BaseAdmin.exclude
    form = MediaAdminForm
    inlines = [MediaDetailAdmin]
    list_display = (
        'display_image',
        'type',
        'title_and_genres',
        'display_rating',
        'launch_date',
        'display_imdb_link',
        'status'
    )
    list_filter = (MediaTypeFilter, MediaGenreFilter, MediaStatusFilter,)
    list_per_page = 5
    model = Media
    resource_class = MediaResource
    search_fields = (
        'title',
        'original_title',
        'media_genre__name'
    )

    def type(self, obj):
        return obj.media_type.name
    type.short_description = 'Type'

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 150px;" />',
                main.settings.BASE_URL + obj.image.url
            )
        else:
            return ''
    display_image.short_description = 'Image'

    def title_and_genres(self, obj):
        edit_url = reverse(
            'admin:entertainment_media_change',
            args=[obj.id]
        )
        return format_html(
            '<a href="{}">{}</a>',
            edit_url, f"{obj.title} | {obj.media_genre.name}"
        )
    title_and_genres.short_description = 'Title and Genre'

    def display_rating(self, obj):
        rating_stars = '⭐' * int(obj.rating)
        return format_html(
            '<span title="{}"><strong>{}</strong></span> ({})',
            obj.rating, rating_stars, obj.rating
        )
    display_rating.short_description = 'Rating'

    def display_imdb_link(self, obj):
        if obj.imdb_link:
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                obj.imdb_link, obj.title
            )
        else:
            return obj.title
    display_imdb_link.short_description = 'IMDB Link'

    def status(self, obj):
        return obj.media_status.name
    status.short_description = 'Status'
