from main.import_export import BaseResource
from entertainment.models import *


class EntertainmentConfigResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + ('name', 'related_field',)
        fields = BaseResource.Meta.fields + ('name', 'related_field',)
        model = EntertainmentConfig


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


class GameResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + (
            'image',
            'title',
            'game_genre',
            'rating',
            'released_date',
            'description',
            'game_status',
        )
        fields = BaseResource.Meta.fields + (
            'image',
            'title',
            'game_genre',
            'rating',
            'released_date',
            'description',
            'game_status',
        )
        model = Game


class MediaResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + (
            'media_type',
            'image',
            'title',
            'original_title',
            'media_genre',
            'rating',
            'launch_date',
            'description',
            'imdb_link',
            'media_status',
        )
        fields = BaseResource.Meta.fields + (
            'media_type',
            'image',
            'title',
            'original_title',
            'media_genre',
            'rating',
            'launch_date',
            'description',
            'imdb_link',
            'media_status',
        )
        model = Media
