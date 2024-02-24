from django.db import models
from main.models import BaseModel


RELATED_FIELDS = [
    ('book_statuses', 'Book status'),
    ('book_genres', 'Book genre'),
    ('book_languages', 'Book languages'),
    ('book_detail_currencies', 'Book details currencies'),
    ('game_statuses', 'Game status'),
    ('game_genres', 'Game genre'),
    ('game_detail_currencies', 'Game details currencies'),
    ('media_statuses', 'Media status'),
    ('media_genres', 'Media genre'),
    ('media_types', 'Media types'),
]


class BookType(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "Book type"
        verbose_name_plural = "Book types"

    def __str__(self):
        return f"{self.name}"


class BookGenre(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "Book genre"
        verbose_name_plural = "Book genres"

    def __str__(self):
        return f"{self.name}"


class BookStatus(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "Book status"
        verbose_name_plural = "Book statuses"

    def __str__(self):
        return f"{self.name}"


class BookLanguage(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "Book type"
        verbose_name_plural = "Book types"

    def __str__(self):
        return f"{self.name}"
