from django.core.validators import MinValueValidator, MaxValueValidator
from django_ckeditor_5.fields import CKEditor5Field
from main.models import *
from settings.models import *


class MovieType(BaseModel, BaseSettingModel):
    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Types"


class MovieGenre(BaseModel, BaseSettingModel):
    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class MovieStatus(BaseModel, BaseSettingModel):
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class Movie(BaseModel):
    movie_type = models.ForeignKey(
        MovieType,
        on_delete=models.CASCADE,
        related_name='movie_types',
        blank=False,
        null=False,
        verbose_name="Type"
    )
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
        indexes = [
            models.Index(fields=["movie_type"], name="movie_type_idx"),
            models.Index(fields=["movie_genre"], name="movie_genre_idx"),
        ]
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
        indexes = [
            models.Index(fields=["movie"], name="movie_idx"),
        ]
        verbose_name = "Movie detail"
        verbose_name_plural = "Movie details"
