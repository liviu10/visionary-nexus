# Generated by Django 5.0.2 on 2024-02-25 16:52

import django.db.models.deletion
import django.utils.timezone
import main.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to=main.utils.upload_to)),
                ('title', models.CharField(max_length=255)),
                ('launch_date', models.DateField(blank=True, null=True)),
                ('album', models.CharField(blank=True, max_length=255, null=True)),
                ('band', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Music',
                'verbose_name_plural': 'Music',
            },
        ),
        migrations.CreateModel(
            name='MusicDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('download_link', models.CharField(blank=True, max_length=255, null=True)),
                ('lyrics_link', models.CharField(blank=True, max_length=255, null=True)),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_details', to='music.music')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Music detail',
                'verbose_name_plural': 'Music details',
            },
        ),
        migrations.CreateModel(
            name='MusicGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
            },
        ),
        migrations.AddField(
            model_name='music',
            name='music_genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_genres', to='music.musicgenre', verbose_name='Genre'),
        ),
    ]
