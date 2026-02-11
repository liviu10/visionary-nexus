from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .models import Type, Genre, Status, Language, Book, Game, Movie


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('id',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category', 'name')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category', 'name')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category', 'id')


@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    list_display = ('title', 'authors', 'book_genre', 'book_status', 'rating', 'user', 'show_image')
    list_filter = ('book_status', 'book_genre', 'book_type', 'book_language', 'user', 'date_added')
    search_fields = ('title', 'authors', 'isbn_13')
    readonly_fields = ('date_added', 'show_image_detail')
    
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

    def show_image(self, obj):
        if obj.goodreads_image_link:
            return format_html('<img src="{}" style="height: 50px; border-radius: 5px;" />', obj.goodreads_image_link)
        return "-"
    show_image.short_description = "Cover"

    def show_image_detail(self, obj):
        if obj.goodreads_image_link:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 5px;" />', obj.goodreads_image_link)
        return "No image link provided"
    show_image_detail.short_description = "Cover Preview"


@admin.register(Game)
class GameAdmin(ImportExportModelAdmin):
    list_display = ('title', 'game_genre', 'game_status', 'rating', 'released_date', 'user', 'show_image')
    list_filter = ('game_status', 'game_genre', 'user', 'released_date')
    search_fields = ('title',)
    readonly_fields = ('show_image_detail',)

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

    def show_image(self, obj):
        if obj.game_image_link:
            return format_html('<img src="{}" style="height: 50px; border-radius: 5px;" />', obj.game_image_link)
        return "-"
    show_image.short_description = "Cover"

    def show_image_detail(self, obj):
        if obj.game_image_link:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 5px;" />', obj.game_image_link)
        return "No image link"
    show_image_detail.short_description = "Cover Preview"


@admin.register(Movie)
class MovieAdmin(ImportExportModelAdmin):
    list_display = ('title', 'movie_type', 'movie_genre', 'movie_status', 'rating', 'launch_date', 'user', 'show_image')
    list_filter = ('movie_status', 'movie_genre', 'movie_type', 'user', 'launch_date')
    search_fields = ('title', 'original_title')
    readonly_fields = ('show_image_detail',)

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

    def show_image(self, obj):
        if obj.movie_image_link:
            return format_html('<img src="{}" style="height: 50px; border-radius: 5px;" />', obj.movie_image_link)
        return "-"
    show_image.short_description = "Poster"

    def show_image_detail(self, obj):
        if obj.movie_image_link:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 5px;" />', obj.movie_image_link)
        return "No image link"
    show_image_detail.short_description = "Poster Preview"