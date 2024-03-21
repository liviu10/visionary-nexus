from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from main.models import *
from settings.models import *


class GameGenre(BaseModel, SettingModel):
    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class GameStatus(BaseModel, SettingModel):
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class Game(BaseModel):
    title = models.CharField(max_length=255, blank=False, null=False)
    game_genre = models.ForeignKey(
        GameGenre,
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
    game_status = models.ForeignKey(
        GameStatus,
        on_delete=models.CASCADE,
        related_name='game_statuses',
        blank=False,
        null=False,
        verbose_name="Status"
    )
    game_link = models.CharField(max_length=255, blank=True, null=True)
    game_image_link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["game_genre"], name="game_genre_idx"),
            models.Index(fields=["game_status"], name="game_status_idx"),
        ]
        verbose_name = "Game"
        verbose_name_plural = "Games"

    def __str__(self):
        return f"Title: {self.title} | Genre: {self.game_genre.name}"


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
    game_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='game_currencies',
        blank=True,
        null=True,
        verbose_name='Currency'
    )

    class Meta:
        indexes = [
            models.Index(fields=["game"], name="game_idx"),
            models.Index(fields=["game_currency"], name="game_currency_idx"),
        ]
        verbose_name = "Game detail"
        verbose_name_plural = "Game details"
