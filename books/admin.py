from django.contrib import admin
from import_export.admin import ImportExportMixin
from main.admin import BaseAdmin
from books.forms import *
from books.import_export import *
from django.utils.html import format_html
import main.settings


@admin.register(BookType)
class BookTypeAdmin(ImportExportMixin, BaseAdmin):
    form = BookTypeAdminForm
    list_display = ('id', 'name',)
    model = BookType
    ordering = ['id']
    resource_class = BookTypeResource
    search_fields = ('name',)


@admin.register(BookLanguage)
class BookLanguageAdmin(ImportExportMixin, BaseAdmin):
    form = BookLanguageAdminForm
    list_display = ('id', 'name',)
    model = BookLanguage
    ordering = ['id']
    resource_class = BookLanguageResource
    search_fields = ('name',)


@admin.register(BookGenre)
class BookGenreAdmin(ImportExportMixin, BaseAdmin):
    form = BookGenreAdminForm
    list_display = ('id', 'name',)
    model = BookGenre
    ordering = ['id']
    resource_class = BookGenreResource
    search_fields = ('name',)


@admin.register(BookStatus)
class BookStatusAdmin(ImportExportMixin, BaseAdmin):
    form = BookStatusAdminForm
    list_display = ('id', 'name',)
    model = BookStatus
    ordering = ['id']
    resource_class = BookStatusResource
    search_fields = ('name',)


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
    list_filter = (
        'book_type',
        'book_language',
        'book_genre',
        'book_status',
    )
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
            'admin:books_book_change',
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
