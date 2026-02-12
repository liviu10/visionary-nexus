from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth.models import User
from .models import Book, Game, Movie, Type, Language, Genre, Status


class BoundUserResourceMixin:
    def __init__(self, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(**kwargs)

    def before_save_instance(self, instance, using_transactions, dry_run):
        if self.user:
            instance.user = self.user
        super().before_save_instance(instance, using_transactions, dry_run)


class BookResource(BoundUserResourceMixin, resources.ModelResource):
    book_type = fields.Field(
        column_name='book_type',
        attribute='book_type',
        widget=ForeignKeyWidget(Type, 'id')
    )
    book_language = fields.Field(
        column_name='book_language',
        attribute='book_language',
        widget=ForeignKeyWidget(Language, 'id')
    )
    book_genre = fields.Field(
        column_name='book_genre',
        attribute='book_genre',
        widget=ForeignKeyWidget(Genre, 'id')
    )
    book_status = fields.Field(
        column_name='book_status',
        attribute='book_status',
        widget=ForeignKeyWidget(Status, 'id')
    )
    user = fields.Field(attribute='user', widget=ForeignKeyWidget(User, 'username'))

    class Meta:
        model = Book
        fields = (
            'book_type', 'book_language', 'authors', 'title', 
            'book_genre', 'rating', 'published_date', 'description', 
            'isbn_13', 'page_count', 'book_status', 'date_added', 
            'date_read', 'goodreads_link', 'goodreads_book_id', 
            'goodreads_image_link'
        )
        import_id_fields = ('title',)


class MovieResource(BoundUserResourceMixin, resources.ModelResource):
    movie_type = fields.Field(
        column_name='movie_type',
        attribute='movie_type',
        widget=ForeignKeyWidget(Type, 'id')
    )
    movie_genre = fields.Field(
        column_name='movie_genre',
        attribute='movie_genre',
        widget=ForeignKeyWidget(Genre, 'id')
    )
    movie_status = fields.Field(
        column_name='movie_status',
        attribute='movie_status',
        widget=ForeignKeyWidget(Status, 'id')
    )
    user = fields.Field(attribute='user', widget=ForeignKeyWidget(User, 'username'))

    class Meta:
        model = Movie
        fields = (
            'movie_type', 'title', 'original_title', 'movie_genre', 
            'rating', 'launch_date', 'description', 'movie_link', 
            'movie_image_link', 'movie_status'
        )
        import_id_fields = ('title',)


class GameResource(BoundUserResourceMixin, resources.ModelResource):
    game_genre = fields.Field(
        column_name='game_genre',
        attribute='game_genre',
        widget=ForeignKeyWidget(Genre, 'id')
    )
    game_status = fields.Field(
        column_name='game_status',
        attribute='game_status',
        widget=ForeignKeyWidget(Status, 'id')
    )
    user = fields.Field(attribute='user', widget=ForeignKeyWidget(User, 'username'))

    class Meta:
        model = Game
        fields = (
            'title', 'game_genre', 'rating', 'released_date',
            'description', 'game_status', 'game_link', 'game_image_link'
        )
        import_id_fields = ('title',)
