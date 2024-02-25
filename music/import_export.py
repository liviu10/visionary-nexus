from main.import_export import BaseResource
from music.models import *


class MusicGenreResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + ('name',)
        fields = BaseResource.Meta.fields + ('name',)
        model = MusicGenre


class MusicResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + (
            'image',
            'title',
            'music_genre',
            'launch_date',
            'album',
            'band',
        )
        fields = BaseResource.Meta.fields + (
            'image',
            'title',
            'music_genre',
            'launch_date',
            'album',
            'band',
        )
        model = Music
