from main.admin import BaseResource
from movies.models import *


class MovieTypeResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + ('name',)
        fields = BaseResource.Meta.fields + ('name',)
        model = MovieType


class MovieGenreResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + ('name',)
        fields = BaseResource.Meta.fields + ('name',)
        model = MovieGenre


class MovieStatusResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + ('name',)
        fields = BaseResource.Meta.fields + ('name',)
        model = MovieStatus


class MovieResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + (
            'movie_type',
            'image',
            'title',
            'original_title',
            'movie_genre',
            'rating',
            'launch_date',
            'description',
            'movie_link',
            'movie_image_link',
            'movie_status',
        )
        fields = BaseResource.Meta.fields + (
            'movie_type',
            'image',
            'title',
            'original_title',
            'movie_genre',
            'rating',
            'launch_date',
            'description',
            'movie_link',
            'movie_image_link',
            'movie_status',
        )
        import_id_fields = ['id',]
        model = Movie
