# Generated by Django 5.0.2 on 2024-03-22 08:10

import main.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        ('settings', '0004_currency_image_language_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'verbose_name': 'Book', 'verbose_name_plural': 'Books'},
        ),
        migrations.AddField(
            model_name='bookdetail',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=main.utils.upload_to),
        ),
        migrations.AddField(
            model_name='bookgenre',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=main.utils.upload_to),
        ),
        migrations.AddField(
            model_name='bookstatus',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=main.utils.upload_to),
        ),
        migrations.AddField(
            model_name='booktype',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=main.utils.upload_to),
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['book_type'], name='book_type_idx'),
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['book_language'], name='book_language_idx'),
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['book_genre'], name='book_genre_idx'),
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['book_status'], name='book_status_idx'),
        ),
        migrations.AddIndex(
            model_name='bookdetail',
            index=models.Index(fields=['book'], name='book_idx'),
        ),
        migrations.AddIndex(
            model_name='bookdetail',
            index=models.Index(fields=['book_currency'], name='book_currency_idx'),
        ),
    ]
