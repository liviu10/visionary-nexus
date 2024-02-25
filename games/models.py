from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from main.models import BaseModel
from main.utils import upload_to
from settings.models import Currency


class GameGenre(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return f"{self.name}"


class GameStatus(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"

    def __str__(self):
        return f"{self.name}"


class Game(BaseModel):
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    game_genre = models.ForeignKey(
        GameGenre,
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
        GameStatus,
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
    game_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='game_currencies',
        blank=True,
        null=True,
        verbose_name='Currency'
    )

    class Meta:
        verbose_name = "Game detail"
        verbose_name_plural = "Game details"
