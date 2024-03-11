from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from main.models import BaseModel
from main.utils import upload_to


class MovieType(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Types"

    def __str__(self):
        return f"{self.name}"


class MovieGenre(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return f"{self.name}"


class MovieStatus(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"

    def __str__(self):
        return f"{self.name}"


class Movie(BaseModel):
    movie_type = models.ForeignKey(
        MovieType,
        on_delete=models.CASCADE,
        related_name='movie_types',
        blank=False,
        null=False,
        verbose_name="Type"
    )
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    original_title = models.CharField(max_length=255, blank=False, null=False)
    movie_genre = models.ForeignKey(
        MovieGenre,
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
    movie_status = models.ForeignKey(
        MovieStatus,
        on_delete=models.CASCADE,
        related_name='movie_statuses',
        blank=False,
        null=False,
        verbose_name="Status"
    )

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return f"Title: {self.title} | Genre: {self.movie_genre.name}"


class MovieDetail(BaseModel):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='movie_details',
        blank=False,
        null=False
    )
    download_link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Movie detail"
        verbose_name_plural = "Movie details"
