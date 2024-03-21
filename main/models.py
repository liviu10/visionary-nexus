from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from main.utils import upload_to


class BaseModel(models.Model):
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
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

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.storage.delete(self.image.name)
        super().delete(*args, **kwargs)


class SettingModel(models.Model):
    name = models.CharField(
        min_length=3,
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
