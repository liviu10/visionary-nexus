from django.db import models
from main.models import BaseModel


class Currency(BaseModel):
    country = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f"{self.code}"


class Language(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __str__(self):
        return f"{self.name}"