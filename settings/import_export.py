from main.import_export import BaseResource
from settings.models import *


class CurrencyResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + (
            'country',
            'currency',
            'code',
        )
        fields = BaseResource.Meta.fields + (
            'country',
            'currency',
            'code',
        )
        model = Currency


class LanguageResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + ('name', 'code',)
        fields = BaseResource.Meta.fields + ('name', 'code',)
        model = Language


class LogTypeResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + (
            'name',
            'description',
            'when',
        )
        fields = BaseResource.Meta.fields + (
            'name',
            'description',
            'when',
        )
        model = LogType


class LogEventResource(BaseResource):
    class Meta:
        export_order = BaseResource.Meta.fields + (
            'log_type',
            'description',
            'request_details',
            'response_details',
            'sql_details',
        )
        fields = BaseResource.Meta.fields + (
            'log_type',
            'description',
            'request_details',
            'response_details',
            'sql_details',
        )
        model = LogEvent
