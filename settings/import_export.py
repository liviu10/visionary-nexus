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
