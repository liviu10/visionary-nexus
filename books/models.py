from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from main.models import BaseModel
from main.utils import upload_to
from settings.models import Currency


class BookType(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Types"

    def __str__(self):
        return f"{self.name}"


class BookLanguage(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __str__(self):
        return f"{self.name}"


class BookGenre(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return f"{self.name}"


class BookStatus(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"

    def __str__(self):
        return f"{self.name}"


class Book(BaseModel):
    book_type = models.ForeignKey(
        BookType,
        on_delete=models.CASCADE,
        related_name='book_types',
        blank=False,
        null=False,
        verbose_name="Type"
    )
    book_language = models.ForeignKey(
        BookLanguage,
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
        BookGenre,
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
        BookStatus,
        on_delete=models.CASCADE,
        related_name='book_statuses',
        blank=False,
        null=False,
        verbose_name="Status"
    )
    date_added = models.DateField(blank=True, null=True)
    date_read = models.DateField(blank=True, null=True)
    goodreads_link = models.CharField(max_length=255, blank=True, null=True)

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
    book_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='book_currencies',
        blank=True,
        null=True,
        verbose_name='Currency'
    )

    class Meta:
        verbose_name = "Book detail"
        verbose_name_plural = "Book details"
