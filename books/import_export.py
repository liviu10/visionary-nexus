from main.admin import BaseResource
from books.models import *


class BookTypeResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + ('name',)
        fields = BaseResource.Meta.fields + ('name',)
        model = BookType


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
            'date_added',
            'date_read',
            'goodreads_link',
            'goodreads_book_id',
            'goodreads_image_link',
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
            'date_added',
            'date_read',
            'goodreads_link',
            'goodreads_book_id',
            'goodreads_image_link',
        )
        model = Book
