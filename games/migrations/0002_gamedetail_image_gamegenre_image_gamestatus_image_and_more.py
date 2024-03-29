# Generated by Django 5.0.2 on 2024-03-22 08:10

import main.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
        ('settings', '0004_currency_image_language_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='gamedetail',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=main.utils.upload_to),
        ),
        migrations.AddField(
            model_name='gamegenre',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=main.utils.upload_to),
        ),
        migrations.AddField(
            model_name='gamestatus',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=main.utils.upload_to),
        ),
        migrations.AddIndex(
            model_name='game',
            index=models.Index(fields=['game_genre'], name='game_genre_idx'),
        ),
        migrations.AddIndex(
            model_name='game',
            index=models.Index(fields=['game_status'], name='game_status_idx'),
        ),
        migrations.AddIndex(
            model_name='gamedetail',
            index=models.Index(fields=['game'], name='game_idx'),
        ),
        migrations.AddIndex(
            model_name='gamedetail',
            index=models.Index(fields=['game_currency'], name='game_currency_idx'),
        ),
    ]
