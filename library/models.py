from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.TextChoices):
    BOOK = 'BOOK', 'Book'
    GAME = 'GAME', 'Game'
    MOVIE = 'MOVIE', 'Movie'


class Type(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=10, choices=Category.choices, default=Category.BOOK, help_text="Select the model this type belongs to")

    class Meta:
        ordering = ('id',)
        verbose_name = "Type"
        verbose_name_plural = "Types"
        indexes = [
            models.Index(fields=["category"], name="type_category_idx"),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Genre(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=10, choices=Category.choices, default=Category.BOOK, help_text="Select the model this genre belongs to")

    class Meta:
        ordering = ('id',)
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        indexes = [
            models.Index(fields=["category"], name="genre_category_idx"),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Status(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=10, choices=Category.choices, default=Category.BOOK, help_text="Select the model this status belongs to")

    class Meta:
        ordering = ('id',)
        verbose_name = "Status"
        verbose_name_plural = "Statuses"
        indexes = [
            models.Index(fields=["category"], name="status_category_idx"),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Language(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('id',)
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        indexes = [
            models.Index(fields=["name"], name="language_name_idx"),
        ]

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    book_type = models.ForeignKey(
        Type, 
        on_delete=models.CASCADE, 
        related_name='books', 
        blank=True, null=True, 
        verbose_name="Type",
        limit_choices_to={'category': Category.BOOK}
    )
    book_language = models.ForeignKey(
        Language, 
        on_delete=models.CASCADE, 
        related_name='books', 
        blank=True, null=True, 
        verbose_name="Language"
    )
    authors = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    book_genre = models.ForeignKey(
        Genre, 
        on_delete=models.CASCADE, 
        related_name='books', 
        blank=True, null=True, 
        verbose_name="Genre",
        limit_choices_to={'category': Category.BOOK}
    )
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    published_date = models.DateField(blank=True, null=True)
    description = CKEditor5Field('Description', config_name='extends', blank=True, null=True)
    isbn_13 = models.CharField(max_length=13, blank=True, null=True)
    page_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    book_status = models.ForeignKey(
        Status, 
        on_delete=models.CASCADE, 
        related_name='books', 
        blank=True, null=True, 
        verbose_name="Status",
        limit_choices_to={'category': Category.BOOK}
    )
    date_added = models.DateField(auto_now_add=True, blank=True, null=True)
    date_read = models.DateField(blank=True, null=True)
    goodreads_link = models.URLField(max_length=500, blank=True, null=True)
    goodreads_book_id = models.PositiveIntegerField(default=0, blank=True, null=True)
    goodreads_image_link = models.URLField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')

    class Meta:
        ordering = ('id',)
        verbose_name = "Book"
        verbose_name_plural = "Books"
        indexes = [
            models.Index(fields=["title"], name="book_title_idx"),
        ]

    def __str__(self):
        return f"{self.authors} - {self.title}"


class Game(models.Model):
    title = models.CharField(max_length=255)
    game_genre = models.ForeignKey(
        Genre, 
        on_delete=models.CASCADE, 
        related_name='games', 
        verbose_name="Genre",
        limit_choices_to={'category': Category.GAME}
    )
    rating = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], 
        blank=True, null=True
    )
    released_date = models.DateField(blank=True, null=True)
    description = CKEditor5Field('Description', config_name='extends', blank=True, null=True)
    game_status = models.ForeignKey(
        Status, 
        on_delete=models.CASCADE, 
        related_name='games', 
        verbose_name="Status",
        limit_choices_to={'category': Category.GAME}
    )
    game_link = models.URLField(max_length=500, blank=True, null=True)
    game_image_link = models.URLField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='games')

    class Meta:
        ordering = ('id',)
        verbose_name = "Game"
        verbose_name_plural = "Games"
        indexes = [
            models.Index(fields=["title"], name="game_title_idx"),
        ]

    def __str__(self):
        genre_name = self.game_genre.name if self.game_genre else "No Genre"
        return f"{self.title} - {genre_name}"


class Movie(models.Model):
    movie_type = models.ForeignKey(
        Type, 
        on_delete=models.CASCADE, 
        related_name='movies', 
        verbose_name="Type",
        limit_choices_to={'category': Category.MOVIE}
    )
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    movie_genre = models.ForeignKey(
        Genre, 
        on_delete=models.CASCADE, 
        related_name='movies', 
        verbose_name="Genre",
        limit_choices_to={'category': Category.MOVIE}
    )
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    launch_date = models.DateField(blank=True, null=True)
    description = CKEditor5Field('Description', config_name='extends', blank=True, null=True)
    movie_link = models.URLField(max_length=500, blank=True, null=True)
    movie_image_link = models.URLField(max_length=500, blank=True, null=True)
    movie_status = models.ForeignKey(
        Status, 
        on_delete=models.CASCADE, 
        related_name='movies', 
        verbose_name="Status",
        limit_choices_to={'category': Category.MOVIE}
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='movies')

    class Meta:
        ordering = ('id',)
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        indexes = [
            models.Index(fields=["title"], name="movie_title_idx"),
        ]

    def __str__(self):
        genre_name = self.movie_genre.name if self.movie_genre else "No Genre"
        return f"{self.title} - {genre_name}"