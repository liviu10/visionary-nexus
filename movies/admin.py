from django.contrib import admin
from import_export.admin import ImportExportMixin
from movies.utils.IMDBScraper import IMDBScraper
from main.admin import BaseAdmin
from movies.forms import *
from movies.import_export import *
from django.utils.html import format_html
import main.settings


@admin.register(MovieType)
class MovieTypeAdmin(ImportExportMixin, BaseAdmin):
    form = MovieTypeAdminForm
    list_display = ('id', 'name',)
    model = MovieType
    ordering = ['id']
    resource_class = MovieTypeResource
    search_fields = ('name',)


@admin.register(MovieGenre)
class MovieGenreAdmin(ImportExportMixin, BaseAdmin):
    form = MovieGenreAdminForm
    list_display = ('id', 'name',)
    model = MovieGenre
    ordering = ['id']
    resource_class = MovieGenreResource
    search_fields = ('name',)


@admin.register(MovieStatus)
class MovieStatusAdmin(ImportExportMixin, BaseAdmin):
    form = MovieStatusAdminForm
    list_display = ('id', 'name',)
    model = MovieStatus
    ordering = ['id']
    resource_class = MovieStatusResource
    search_fields = ('name',)


class MovieDetailAdmin(admin.TabularInline):
    exclude = BaseAdmin.exclude
    extra = 0
    form = MovieDetailAdminForm
    model = MovieDetail


@admin.register(Movie)
class MovieAdmin(ImportExportMixin, BaseAdmin):
    exclude = BaseAdmin.exclude
    form = MovieAdminForm
    inlines = [MovieDetailAdmin]
    list_display = (
        'display_image',
        'type',
        'title_and_genres',
        'display_rating',
        'launch_date',
        'display_movie_link',
        'status'
    )
    list_filter = ('movie_type', 'movie_genre', 'movie_status',)
    list_per_page = 5
    model = Movie
    resource_class = MovieResource
    search_fields = (
        'title',
        'original_title',
        'movie_genre__name'
    )
    actions = [
        'update_details_from_imdb',
    ]

    def type(self, obj):
        return obj.movie_type.name
    type.short_description = 'Type'

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 150px;" />',
                main.settings.BASE_URL + obj.image.url
            )
        elif obj.game_image_link:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 150px;" />',
                obj.movie_image_link
            )
        else:
            return ''
    display_image.short_description = 'Image'

    def title_and_genres(self, obj):
        edit_url = reverse(
            'admin:movies_movie_change',
            args=[obj.id]
        )
        return format_html(
            '<a href="{}">{}</a>',
            edit_url, f"{obj.title} | {obj.movie_genre.name}"
        )
    title_and_genres.short_description = 'Title and Genre'

    def display_rating(self, obj):
        rating_stars = '⭐' * int(obj.rating)
        return format_html(
            '<span title="{}"><strong>{}</strong></span> ({})',
            obj.rating, rating_stars, obj.rating
        )
    display_rating.short_description = 'Rating'

    def display_movie_link(self, obj):
        if obj.imdb_link:
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                obj.imdb_link, obj.title
            )
        else:
            return obj.title
    display_movie_link.short_description = 'IMDB Link'

    def status(self, obj):
        return obj.movie_status.name
    status.short_description = 'Status'

    def update_details_from_imdb(self, request, queryset):
        for movie in queryset:
            movie_details = IMDBScraper(movie).get_movie_details()
            movie.save()
        self.message_user(request, "Successfully updated details for selected movies.")
    update_details_from_imdb.short_description = 'Update details from IMDB'
