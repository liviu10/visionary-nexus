from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from main.utils import upload_to


class BaseModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["id"], name="id_idx"),
            models.Index(fields=["user"], name="user_idx"),
        ]
        ordering = ('id',)


class BaseSettingModel(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["id"], name="id_idx"),
        ]
        ordering = ('id',)

    def __str__(self):
        return self.name
