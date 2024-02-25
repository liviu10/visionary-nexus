from main.import_export import BaseResource
from books.models import *


class BookTypeResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + ('name',)
        fields = BaseResource.Meta.fields + ('name',)
        model = BookType


class BookLanguageResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + ('name',)
        fields = BaseResource.Meta.fields + ('name',)
        model = BookLanguage


class BookGenreResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + ('name',)
        fields = BaseResource.Meta.fields + ('name',)
        model = BookGenre


class BookStatusResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + ('name',)
        fields = BaseResource.Meta.fields + ('name',)
        model = BookStatus


class BookResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + (
            'book_type',
            'book_language',
            'authors',
            'image',
            'title',
            'book_genre',
            'rating',
            'published_date',
            'description',
            'isbn_13',
            'page_count',
            'book_status',
        )
        fields = BaseResource.Meta.fields + (
            'book_type',
            'book_language',
            'authors',
            'image',
            'title',
            'book_genre',
            'rating',
            'published_date',
            'description',
            'isbn_13',
            'page_count',
            'book_status',
        )
        model = Book
