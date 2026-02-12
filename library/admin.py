from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .models import Type, Genre, Status, Language, Book, Game, Movie
from .resources import GameResource, BookResource, MovieResource


class LanguageAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    def has_module_permission(self, request): return False

class TypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    def has_module_permission(self, request): return False

class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    def has_module_permission(self, request): return False

class StatusAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    def has_module_permission(self, request): return False

admin.site.register(Language, LanguageAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Status, StatusAdmin)


class UserImportMixin:
    def get_resource_kwargs(self, request, *args, **kwargs):
        kwargs = super().get_resource_kwargs(request, *args, **kwargs)
        kwargs.update({"user": request.user})
        return kwargs

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Book)
class BookAdmin(UserImportMixin, ImportExportModelAdmin):
    resource_class = BookResource
    list_display = ('title', 'authors', 'book_genre', 'book_status', 'rating', 'user', 'show_image')
    list_filter = ('book_status', 'book_genre', 'book_type', 'book_language', 'user', 'date_added')
    search_fields = ('title', 'authors', 'isbn_13')
    readonly_fields = ('date_added', 'show_image_detail', 'user')
    autocomplete_fields = ('book_type', 'book_language', 'book_genre', 'book_status')
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'authors', 'book_type', 'book_language', 'user')
        }),
        ('Content Details', {
            'fields': ('description', 'book_genre', 'page_count', 'isbn_13', 'published_date')
        }),
        ('Status & Rating', {
            'fields': ('book_status', 'rating', 'date_read', 'date_added')
        }),
        ('Media & Links', {
            'fields': ('goodreads_link', 'goodreads_book_id', 'goodreads_image_link', 'show_image_detail')
        }),
    )

    @admin.display(description="Cover")
    def show_image(self, obj):
        if obj.goodreads_image_link:
            return format_html('<img src="{}" style="height: 50px; border-radius: 5px;" />', obj.goodreads_image_link)
        return "-"

    @admin.display(description="Cover Preview")
    def show_image_detail(self, obj):
        if obj.goodreads_image_link:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 5px;" />', obj.goodreads_image_link)
        return "No image link provided"


@admin.register(Game)
class GameAdmin(UserImportMixin, ImportExportModelAdmin):
    resource_class = GameResource
    list_display = ('title', 'game_genre', 'game_status', 'rating', 'released_date', 'user', 'show_image')
    list_filter = ('game_status', 'game_genre', 'user', 'released_date')
    search_fields = ('title',)
    readonly_fields = ('show_image_detail', 'user')
    autocomplete_fields = ('game_genre', 'game_status')
    fieldsets = (
        ('Game Info', {
            'fields': ('title', 'game_genre', 'released_date', 'user')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Status & Rating', {
            'fields': ('game_status', 'rating')
        }),
        ('Links & Media', {
            'fields': ('game_link', 'game_image_link', 'show_image_detail')
        }),
    )

    @admin.display(description="Cover")
    def show_image(self, obj):
        if obj.game_image_link:
            return format_html('<img src="{}" style="height: 50px; border-radius: 5px;" />', obj.game_image_link)
        return "-"

    @admin.display(description="Cover Preview")
    def show_image_detail(self, obj):
        if obj.game_image_link:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 5px;" />', obj.game_image_link)
        return "No image link"


@admin.register(Movie)
class MovieAdmin(UserImportMixin, ImportExportModelAdmin):
    resource_class = MovieResource
    list_display = ('title', 'movie_type', 'movie_genre', 'movie_status', 'rating', 'launch_date', 'user', 'show_image')
    list_filter = ('movie_status', 'movie_genre', 'movie_type', 'user', 'launch_date')
    search_fields = ('title', 'original_title')
    readonly_fields = ('show_image_detail', 'user')
    autocomplete_fields = ('movie_type', 'movie_genre', 'movie_status')
    fieldsets = (
        ('Movie Info', {
            'fields': ('title', 'original_title', 'movie_type', 'movie_genre', 'launch_date', 'user')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Status & Rating', {
            'fields': ('movie_status', 'rating')
        }),
        ('Links & Media', {
            'fields': ('movie_link', 'movie_image_link', 'show_image_detail')
        }),
    )

    @admin.display(description="Poster")
    def show_image(self, obj):
        if obj.movie_image_link:
            return format_html('<img src="{}" style="height: 50px; border-radius: 5px;" />', obj.movie_image_link)
        return "-"

    @admin.display(description="Poster Preview")
    def show_image_detail(self, obj):
        if obj.movie_image_link:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 5px;" />', obj.movie_image_link)
        return "No image link"