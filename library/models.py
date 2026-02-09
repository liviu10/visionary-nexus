from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_ckeditor_5.fields import CKEditor5Field
from settings.models import Language


class Type(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        indexes = [
            models.Index(fields=["id"], name="id_idx"),
        ]
        ordering = ('id',)
        verbose_name = "Type"
        verbose_name_plural = "Types"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        indexes = [
            models.Index(fields=["id"], name="id_idx"),
        ]
        ordering = ('id',)
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        indexes = [
            models.Index(fields=["id"], name="id_idx"),
        ]
        ordering = ('id',)
        verbose_name = "Status"
        verbose_name_plural = "Statuses"

    def __str__(self):
        return self.name


class Book(models.Model):
    book_type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name='book_types',
        blank=True,
        null=True,
        verbose_name="Type"
    )
    book_language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name='book_languages',
        blank=True,
        null=True,
        verbose_name="Language"
    )
    authors = models.CharField(max_length=255, blank=False, null=False)
    title = models.CharField(max_length=255, blank=False, null=False)
    book_genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='book_genres',
        blank=True,
        null=True,
        verbose_name="Genre"
    )
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    published_date = models.DateField(blank=True, null=True)
    description = CKEditor5Field('Description', config_name='extends', blank=True, null=True)
    isbn_13 = models.CharField(max_length=13, blank=True, null=True)
    page_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    book_status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='book_statuses',
        blank=True,
        null=True,
        verbose_name="Status"
    )
    date_added = models.DateField(blank=True, null=True)
    date_read = models.DateField(blank=True, null=True)
    goodreads_link = models.CharField(max_length=255, blank=True, null=True)
    goodreads_book_id = models.PositiveIntegerField(default=0, blank=True, null=True)
    goodreads_image_link = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["id"], name="id_idx"),
            models.Index(fields=["book_type"], name="book_type_idx"),
            models.Index(fields=["book_language"], name="book_language_idx"),
            models.Index(fields=["title"], name="title_idx"),
            models.Index(fields=["book_genre"], name="book_genre_idx"),
            models.Index(fields=["book_status"], name="book_status_idx"),
            models.Index(fields=["user"], name="user_idx"),
        ]
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"Authors: {self.authors} | Title: {self.title}"


class Game(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='game_genres',
        blank=False,
        null=False,
        verbose_name="Genre"
    )
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        blank=True,
        null=True
    )
    released_date = models.DateField(blank=True, null=True)
    description = CKEditor5Field('Description', config_name='extends', blank=True, null=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='game_statuses',
        blank=False,
        null=False,
        verbose_name="Status"
    )
    game_link = models.CharField(max_length=255, blank=True, null=True)
    game_image_link = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["id"], name="id_idx"),
            models.Index(fields=["title"], name="title_idx"),
            models.Index(fields=["genre"], name="genre_idx"),
            models.Index(fields=["status"], name="status_idx"),
            models.Index(fields=["user"], name="user_idx"),
        ]
        verbose_name = "Game"
        verbose_name_plural = "Games"

    def __str__(self):
        return f"Title: {self.title} | Genre: {self.game_genre.name}"


class Movie(models.Model):
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name='movie_types',
        blank=False,
        null=False,
        verbose_name="Type"
    )
    title = models.CharField(max_length=255, blank=False, null=False)
    original_title = models.CharField(max_length=255, blank=False, null=False)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='movie_genres',
        blank=False,
        null=False,
        verbose_name="Genre"
    )
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    launch_date = models.DateField(blank=True, null=True)
    description = CKEditor5Field('Description', config_name='extends', blank=True, null=True)
    movie_link = models.CharField(max_length=255, blank=True, null=True)
    movie_image_link = models.CharField(max_length=255, blank=True, null=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='movie_statuses',
        blank=False,
        null=False,
        verbose_name="Status"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["id"], name="id_idx"),
            models.Index(fields=["title"], name="title_idx"),
            models.Index(fields=["type"], name="type_idx"),
            models.Index(fields=["genre"], name="genre_idx"),
            models.Index(fields=["status"], name="status_idx"),
            models.Index(fields=["user"], name="user_idx"),
        ]
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return f"Title: {self.title} | Genre: {self.genre.name}"
