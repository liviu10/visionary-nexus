from django.core.validators import MinValueValidator, MaxValueValidator
from django_ckeditor_5.fields import CKEditor5Field
from main.models import *
from settings.models import *


class BookType(BaseModel, BaseSettingModel):
    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Types"


class BookGenre(BaseModel, BaseSettingModel):
    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class BookStatus(BaseModel, BaseSettingModel):
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"


class Book(BaseModel):
    book_type = models.ForeignKey(
        BookType,
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
        blank=True,
        null=True,
        verbose_name="Status"
    )
    date_added = models.DateField(blank=True, null=True)
    date_read = models.DateField(blank=True, null=True)
    goodreads_link = models.CharField(max_length=255, blank=True, null=True)
    goodreads_book_id = models.PositiveIntegerField(default=0, blank=True, null=True)
    goodreads_image_link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["book_type"], name="book_type_idx"),
            models.Index(fields=["book_language"], name="book_language_idx"),
            models.Index(fields=["book_genre"], name="book_genre_idx"),
            models.Index(fields=["book_status"], name="book_status_idx"),
        ]
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"Authors: {self.authors} | Title: {self.title}"


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
        indexes = [
            models.Index(fields=["book"], name="book_idx"),
            models.Index(fields=["book_currency"], name="book_currency_idx"),
        ]
        verbose_name = "Book detail"
        verbose_name_plural = "Book details"
