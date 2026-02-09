from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from games.models import *


@receiver(pre_save, sender=Game)
def update_game_status(sender, instance, **kwargs):
    today = timezone.now().date()

    if instance.released_date and instance.released_date == today:
        instance.game_status_id = 2
