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
    list_display = ('id', 'name', 'code',)
    model = BookLanguage
    ordering = ['id']
    resource_class = BookLanguageResource
    search_fields = ('name', 'code',)


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
        'display_google_image',
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
        'update_book_details',
    ]

    def display_google_image(self, obj):
        if obj.google_image_link:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 150px;" />',
                obj.google_image_link
            )
        else:
            return ''
    display_google_image.short_description = 'Image'

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

    def update_book_details(self, request, queryset):
        field_mapping = {
            'book_type': {
                'google_field': 'printType',
                'processor': lambda x: BookType.objects.filter(name=x.capitalize()).first()
            },
            'book_language': {
                'google_field': 'language',
                'processor': lambda x: BookLanguage.objects.filter(code=x).first()
            },
            'google_image_link': {
                'google_field': 'imageLinks',
                'processor': lambda x: x['thumbnail']
            },
            'book_genre': {
                'google_field': 'categories',
                'processor': lambda x: BookGenre.objects.filter(name=x[0].capitalize()).first()
            },
            'published_date': {
                'google_field': 'publishedDate',
                'processor': lambda x: x
            },
            'description': {
                'google_field': 'description',
                'processor': lambda x: x
            },
            'page_count': {
                'google_field': 'pageCount',
                'processor': lambda x: x
            },
        }

        for book in queryset:
            book_details = GoogleBooks(book).get_book_details()
            if book_details is not None:
                for model_field, config in field_mapping.items():
                    google_field = config['google_field']
                    processor = config['processor']
                    value = book_details.get(google_field)
                    if value is not None:
                        setattr(book, model_field, processor(value))
                book.save()
            else:
                print(f"Unable to find book details {book.authors} | {book.title}. Saving was skipped!")
        self.message_user(request, f'Successfully updated details for selected books.')
    update_book_details.short_description = 'Update details for selected'
