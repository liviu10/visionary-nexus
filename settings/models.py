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


class LogType(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    when = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Log type"
        verbose_name_plural = "Log types"

    def __str__(self):
        return self.name


class LogEvent(BaseModel):
    log_type = models.ForeignKey(
        LogType,
        on_delete=models.CASCADE,
        related_name='log_types',
        blank=False,
        null=False
    )
    description = models.CharField(max_length=255, blank=True, null=True)
    request_details = models.JSONField(blank=True, null=True)
    response_details = models.JSONField(blank=True, null=True)
    sql_details = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Log event"
        verbose_name_plural = "Log events"

    def __str__(self):
        return self.log_type.name
