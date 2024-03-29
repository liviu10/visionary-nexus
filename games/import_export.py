from main.admin import BaseResource
from games.models import *


class GameGenreResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + ('name',)
        fields = BaseResource.Meta.fields + ('name',)
        model = GameGenre


class GameStatusResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + ('name',)
        fields = BaseResource.Meta.fields + ('name',)
        model = GameStatus


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
            'game_link',
            'game_image_link',
        )
        fields = BaseResource.Meta.fields + (
            'image',
            'title',
            'game_genre',
            'rating',
            'released_date',
            'description',
            'game_status',
            'game_link',
            'game_image_link',
        )
        model = Game
