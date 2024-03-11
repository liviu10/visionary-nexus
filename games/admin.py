from django.contrib import admin
from import_export.admin import ImportExportMixin
from games.utils.SteamScraper import SteamScraper
from main.admin import BaseAdmin
from games.forms import *
from games.import_export import *
from django.utils.html import format_html
import main.settings


@admin.register(GameGenre)
class GameGenreAdmin(ImportExportMixin, BaseAdmin):
    form = GameGenreAdminForm
    list_display = ('id', 'name',)
    model = GameGenre
    ordering = ['id']
    resource_class = GameGenreResource
    search_fields = ('name',)


@admin.register(GameStatus)
class GameStatusAdmin(ImportExportMixin, BaseAdmin):
    form = GameStatusAdminForm
    list_display = ('id', 'name',)
    model = GameStatus
    ordering = ['id']
    resource_class = GameStatusResource
    search_fields = ('name',)


class GameDetailAdmin(admin.TabularInline):
    exclude = BaseAdmin.exclude
    extra = 0
    form = GameDetailAdminForm
    model = GameDetail


@admin.register(Game)
class GameAdmin(ImportExportMixin, BaseAdmin):
    exclude = BaseAdmin.exclude
    form = GameAdminForm
    inlines = [GameDetailAdmin]
    list_display = (
        'display_image',
        'title_and_genres',
        'display_rating',
        'released_date',
        'status'
    )
    list_filter = ('game_genre', 'game_status',)
    list_per_page = 5
    model = Game
    resource_class = GameResource
    search_fields = (
        'title',
        'game_genre__name'
    )
    actions = [
        'update_details_from_steam',
    ]

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 150px;" />',
                main.settings.BASE_URL + obj.image.url
            )
        elif obj.game_image_link:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 150px;" />',
                obj.game_image_link
            )
        else:
            return ''
    display_image.short_description = 'Image'

    def title_and_genres(self, obj):
        edit_url = reverse(
            'admin:games_game_change',
            args=[obj.id]
        )
        return format_html(
            '<a href="{}">{}</a>',
            edit_url, f"{obj.title} | {obj.game_genre.name}"
        )
    title_and_genres.short_description = 'Title and Genre'

    def display_rating(self, obj):
        rating_stars = '⭐' * int(obj.rating)
        return format_html(
            '<span title="{}"><strong>{}</strong></span> ({})',
            obj.rating, rating_stars, obj.rating
        )
    display_rating.short_description = 'Rating'

    def status(self, obj):
        return obj.game_status.name
    status.short_description = 'Status'

    def update_details_from_steam(self, request, queryset):
        for game in queryset:
            game_details = SteamScraper(game).get_game_details()
            game.save()
        self.message_user(request, "Successfully updated details for selected games.")
    update_details_from_steam.short_description = 'Update details from Steam'
