# Generated by Django 5.0.2 on 2024-02-27 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_booklanguage_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='google_image_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
