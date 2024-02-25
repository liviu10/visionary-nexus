from django.db import models
from main.models import BaseModel
from main.utils import upload_to


class MusicGenre(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return f"{self.name}"


class Music(BaseModel):
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    music_genre = models.ForeignKey(
        MusicGenre,
        on_delete=models.CASCADE,
        related_name='music_genres',
        blank=False,
        null=False,
        verbose_name="Genre"
    )
    launch_date = models.DateField(blank=True, null=True)
    album = models.CharField(max_length=255, blank=True, null=True)
    band = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Music"
        verbose_name_plural = "Music"

    def __str__(self):
        return f"Title: {self.title} | Band: {self.band} | Genre: {self.music_genre.name}"


class MusicDetail(BaseModel):
    music = models.ForeignKey(
        Music,
        on_delete=models.CASCADE,
        related_name='music_details',
        blank=False,
        null=False
    )
    download_link = models.CharField(max_length=255, blank=True, null=True)
    lyrics_link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Music detail"
        verbose_name_plural = "Music details"
