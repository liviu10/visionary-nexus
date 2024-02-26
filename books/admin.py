from django.contrib import admin
from import_export.admin import ImportExportMixin
from books.utils.GoogleBooks import GoogleBooks
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
    list_per_page = 50
    model = Book
    resource_class = BookResource
    search_fields = (
        'title',
        'authors',
        'isbn_13',
        'book_genre__name'
    )
    actions = [
        'update_book_type_book',
        'update_book_type_e_book',
        'update_book_type_audio',
        'update_book_description',
    ]

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
        return obj.book_status.name
    status.short_description = 'Status'

    def update_book_type_book(self, request, queryset):
        book_type_book = BookType.objects.all().filter(name='Book').first()
        for book in queryset:
            book.book_type = book_type_book
            book.save()
    update_book_type_book.short_description = 'Update selected to book'

    def update_book_type_e_book(self, request, queryset):
        book_type_e_book = BookType.objects.all().filter(name='E-Book').first()
        for book in queryset:
            book.book_type = book_type_e_book
            book.save()
    update_book_type_e_book.short_description = 'Update selected to e-book'

    def update_book_type_audio(self, request, queryset):
        book_type_audio = BookType.objects.all().filter(name='Audio Book').first()
        for book in queryset:
            book.book_type = book_type_audio
            book.save()
    update_book_type_audio.short_description = 'Update selected to audio book'

    def update_book_description(self, request, queryset):
        google_books_api = main.settings.GOOGLE_BOOKS_API_ENDPOINT
        google_books_api_key = main.settings.GOOGLE_BOOKS_API_KEY
        for book in queryset:
            description_by_author_and_title = GoogleBooks(book).get_google_book_description()
            print(f"Google Book: {description_by_author_and_title}")
            book.description = description_by_author_and_title
            book.save()
        self.message_user(request, f'Successfully updated description for selected books.')
    update_book_description.short_description = 'Update description for selected books'
