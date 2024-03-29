from django.contrib import admin
from import_export.admin import ImportExportMixin
from games.utils.SteamScraper import SteamScraper
from main.admin import BaseAdmin, BaseSettingAdmin
from games.forms import *
from games.import_export import *
from django.utils.html import format_html
import main.settings


@admin.register(GameGenre)
class GameGenreAdmin(ImportExportMixin, BaseAdmin):
    form = GameGenreAdminForm
    list_display = BaseSettingAdmin.list_display
    model = GameGenre
    ordering = BaseSettingAdmin.ordering
    resource_class = GameGenreResource
    search_fields = BaseSettingAdmin.search_fields


@admin.register(GameStatus)
class GameStatusAdmin(ImportExportMixin, BaseAdmin):
    form = GameStatusAdminForm
    list_display = BaseSettingAdmin.list_display
    model = GameStatus
    ordering = BaseSettingAdmin.ordering
    resource_class = GameStatusResource
    search_fields = BaseSettingAdmin.search_fields


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
    title_and_genres.admin_order_field = 'title'

    def display_rating(self, obj):
        rating_stars = '⭐' * int(obj.rating)
        return format_html(
            '<span title="{}"><strong>{}</strong></span> ({})',
            obj.rating, rating_stars, obj.rating
        )
    display_rating.short_description = 'Rating'
    display_rating.admin_order_field = 'rating'

    def status(self, obj):
        return obj.game_status.name
    status.short_description = 'Status'
    status.admin_order_field = 'game_status__name'

    def update_details_from_steam(self, request, queryset):
        for game in queryset:
            game_details = SteamScraper(game).get_game_details()

            # Rating
            if 'rating' in game_details and (game.rating is None or game.rating == 0):
                game.rating = game_details['rating']
            # Description
            if 'description' in game_details and (not game.description or game.description.isspace()):
                game.description = game_details['description']
            # Cover URL
            if 'cover_url' in game_details and game.game_image_link is None:
                game.game_image_link = game_details['cover_url']

            game.save()
        self.message_user(request, "Successfully updated details for selected games.")
    update_details_from_steam.short_description = 'Update details from Steam'
