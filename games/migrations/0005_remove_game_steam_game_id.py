# Generated by Django 5.0.2 on 2024-03-11 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_alter_game_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='steam_game_id',
        ),
    ]
