from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from main.models import BaseModel
from entertainment.utils import upload_to


RELATED_FIELDS = [
    ('book_statuses', 'Book status'),
    ('book_genres', 'Book genre'),
    ('book_types', 'Book types'),
    ('book_languages', 'Book languages'),
    ('book_detail_currencies', 'Book details currencies'),
    ('game_statuses', 'Game status'),
    ('game_genres', 'Game genre'),
    ('game_detail_currencies', 'Game details currencies'),
    ('media_statuses', 'Media status'),
    ('media_genres', 'Media genre'),
    ('media_types', 'Media types'),
]


class EntertainmentConfig(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    related_field = models.CharField(max_length=50, choices=RELATED_FIELDS)

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"

    def __str__(self):
        return f"{self.name}"


class Book(BaseModel):
    book_type = models.ForeignKey(
        EntertainmentConfig,
        on_delete=models.CASCADE,
        related_name='book_types',
        blank=False,
        null=False,
        verbose_name="Type"
    )
    book_language = models.ForeignKey(
        EntertainmentConfig,
        on_delete=models.CASCADE,
        related_name='book_languages',
        blank=False,
        null=False,
        verbose_name="Language"
    )
    authors = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    book_genre = models.ForeignKey(
        EntertainmentConfig,
        on_delete=models.CASCADE,
        related_name='book_genres',
        blank=False,
        null=False,
        verbose_name="Genre"
    )
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    published_date = models.DateField(blank=True, null=True)
    description = CKEditor5Field('Description', config_name='extends', blank=True, null=True)
    isbn_13 = models.CharField(max_length=13, blank=True, null=True)
    page_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    book_status = models.ForeignKey(
        EntertainmentConfig,
        on_delete=models.CASCADE,
        related_name='book_statuses',
        blank=False,
        null=False,
        verbose_name="Status"
    )

    class Meta:
        ordering = ('id',)
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"Authors: {self.authors} | Title: {self.title}"

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.storage.delete(self.image.name)
        super().delete(*args, **kwargs)


class BookDetail(BaseModel):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='book_details',
        blank=False,
        null=False
    )
    buy_link = models.CharField(max_length=255, blank=True, null=True)
    download_link = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=30, decimal_places=2, default=0.00)
    book_detail_currency = models.ForeignKey(
        EntertainmentConfig,
        on_delete=models.CASCADE,
        related_name='book_detail_currencies',
        blank=True,
        null=True,
        verbose_name='Currency'
    )

    class Meta:
        verbose_name = "Book detail"
        verbose_name_plural = "Book details"


class Game(BaseModel):
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    game_genre = models.ForeignKey(
        EntertainmentConfig,
        on_delete=models.CASCADE,
        related_name='game_genres',
        blank=False,
        null=False,
        verbose_name="Genre"
    )
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    released_date = models.DateField(blank=True, null=True)
    description = CKEditor5Field('Description', config_name='extends', blank=True, null=True)
    game_status = models.ForeignKey(
        EntertainmentConfig,
        on_delete=models.CASCADE,
        related_name='game_statuses',
        blank=False,
        null=False,
        verbose_name="Status"
    )

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"

    def __str__(self):
        return f"Title: {self.title} | Genre: {self.game_genre.name}"

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.storage.delete(self.image.name)
        super().delete(*args, **kwargs)


class GameDetail(BaseModel):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='game_details',
        blank=False,
        null=False
    )
    buy_link = models.CharField(max_length=255, blank=True, null=True)
    download_link = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=30, decimal_places=2, default=0.00)
    game_detail_currency = models.ForeignKey(
        EntertainmentConfig,
        on_delete=models.CASCADE,
        related_name='game_detail_currencies',
        blank=True,
        null=True,
        verbose_name='Currency'
    )

    class Meta:
        verbose_name = "Game detail"
        verbose_name_plural = "Game details"


class Media(BaseModel):
    media_type = models.ForeignKey(
        EntertainmentConfig,
        on_delete=models.CASCADE,
        related_name='media_types',
        blank=False,
        null=False,
        verbose_name="Type"
    )
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    original_title = models.CharField(max_length=255, blank=False, null=False)
    media_genre = models.ForeignKey(
        EntertainmentConfig,
        on_delete=models.CASCADE,
        related_name='media_genres',
        blank=False,
        null=False,
        verbose_name="Genre"
    )
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    launch_date = models.DateField(blank=True, null=True)
    description = CKEditor5Field('Description', config_name='extends', blank=True, null=True)
    imdb_link = models.CharField(max_length=255, blank=True, null=True)
    media_status = models.ForeignKey(
        EntertainmentConfig,
        on_delete=models.CASCADE,
        related_name='media_statuses',
        blank=False,
        null=False,
        verbose_name="Status"
    )

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Media"

    def __str__(self):
        return f"Title: {self.title} | Genre: {self.media_genre.name}"


class MediaDetail(BaseModel):
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name='media_details',
        blank=False,
        null=False
    )
    download_link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Media detail"
        verbose_name_plural = "Media details"
