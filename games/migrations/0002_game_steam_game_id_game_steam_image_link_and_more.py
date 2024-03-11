# Generated by Django 5.0.2 on 2024-03-11 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='steam_game_id',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='steam_image_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='steam_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]