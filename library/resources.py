from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth.models import User
from .models import Genre, Language, Status, Type, Game

class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre
        import_id_fields = ('name', 'category')
        fields = ('name', 'category')

class LanguageResource(resources.ModelResource):
    class Meta:
        model = Language
        import_id_fields = ('name', 'code')
        fields = ('name', 'code')

class StatusResource(resources.ModelResource):
    class Meta:
        model = Status
        import_id_fields = ('name', 'category')
        fields = ('name', 'category')

class TypeResource(resources.ModelResource):
    class Meta:
        model = Type
        fields = ('name', 'category')
        import_id_fields = ('name', 'category')

class GameResource(resources.ModelResource):
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
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )

    class Meta:
        model = Game
        fields = ('title', 'game_genre', 'rating', 'released_date', 'description', 'game_status', 'game_link', 'game_image_link', 'user')
        import_id_fields = ('title',)
