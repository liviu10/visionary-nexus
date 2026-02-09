from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from movies.models import *


@receiver(pre_save, sender=Movie)
def update_movie_status(sender, instance, **kwargs):
    today = timezone.now().date()

    if instance.launch_date and instance.launch_date == today:
        instance.movie_status_id = 2
