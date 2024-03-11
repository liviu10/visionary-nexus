from django.contrib import admin
from import_export.admin import ImportExportMixin
from books.utils.GoodreadsScraper import GoodreadsScraper
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
        'date_added',
        'date_read',
        'isbn_13',
        'pages',
        'status',
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
    actions = [
        'update_goodreads_book_link',
        'update_details_from_goodreads',
    ]

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 150px;" />',
                main.settings.BASE_URL + obj.image.url
            )
        elif obj.goodreads_image_link:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 150px;" />',
                obj.goodreads_image_link
            )
        else:
            return ''
    display_image.short_description = 'Image'

    def type(self, obj):
        if obj.book_genre:
            return obj.book_type.name
        else:
            return ''
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
        if obj.book_genre:
            return obj.book_genre.name
        else:
            return ''
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
        if obj.book_genre:
            return obj.book_status.name
        else:
            return ''
    status.short_description = 'Status'

    def update_goodreads_book_link(self, request, queryset):
        for book in queryset:
            if book.goodreads_link:
                print(f"The book {book} already have a goodreads link! Scraping was skipped!")
            else:
                goodreads_link = GoodreadsScraper(book).get_goodreads_link()
                book.goodreads_link = goodreads_link
                book.save()
        self.message_user(request, "Successfully updated details for selected books.")
    update_goodreads_book_link.short_description = 'Update Goodreads book link'

    def update_details_from_goodreads(self, request, queryset):
        for book in queryset:
            book_details = GoodreadsScraper(book).get_goodreads_details()

            # Language
            if 'language' in book_details and book.book_language is None:
                language_instance = Language.objects.filter(name=book_details['language']).first()
                if language_instance:
                    book.book_language = language_instance
            # Authors
            if 'authors' in book_details and book.authors is None:
                book.authors = book_details['authors']
            # Cover URL
            if 'cover_url' in book_details and book.goodreads_image_link is None:
                book.goodreads_image_link = book_details['cover_url']
            # Title
            if 'title' in book_details and book.title is None:
                book.title = book_details['title']
            # Genre
            if 'genre' in book_details and book.book_genre is None:
                genre_instance = BookGenre.objects.filter(name=book_details['genre']).first()
                if genre_instance:
                    book.genre = genre_instance
            # Rating
            if 'ratings' in book_details and book.rating is None:
                book.rating = book_details['rating']
            # Published Date
            if 'published_date' in book_details and book.published_date is None:
                book.published_date = book_details['published_date']
            # Description
            if 'description' in book_details and book.description is None:
                book.description = book_details['description']
            # ISBN
            if 'isbn' in book_details and book.isbn_13 is None:
                book.isbn_13 = book_details['isbn']
            # Page count
            if 'page_count' in book_details and book.page_count is None:
                book.page_count = book_details['page_count']
            # Status
            if 'status' in book_details and book.book_status is None:
                book_status_instance = BookStatus.objects.filter(name=book_details['status']).first()
                if book_status_instance:
                    book.book_status = book_status_instance
            book.save()
        self.message_user(request, "Successfully updated details for selected books.")
    update_details_from_goodreads.short_description = 'Update details from Goodreads'
