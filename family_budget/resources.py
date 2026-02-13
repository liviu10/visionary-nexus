import logging
import joblib
import numpy as np
from import_export import resources, fields, widgets
from import_export.widgets import ForeignKeyWidget, DateWidget, DecimalWidget
from django.db.models import Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from django.contrib.auth.models import User
from .models import AccountTransaction, Category, Subcategory, Account, Currency, AmortizationSchedule
import tablib
import re
from .models import AccountTransaction


logger = logging.getLogger(__name__)


class BoundUserResourceMixin:
    def __init__(self, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(**kwargs)

    def before_save_instance(self, instance, using_transactions, dry_run):
        if self.user:
            instance.user = self.user
        super().before_save_instance(instance, using_transactions, dry_run)


class CurrencyResource(BoundUserResourceMixin, resources.ModelResource):
    class Meta:
        model = Currency
        fields = ('country', 'currency', 'code')
        import_id_fields = ('code',)


class CategoryResource(BoundUserResourceMixin, resources.ModelResource):
    class Meta:
        model = Category
        fields = ('name',)
        import_id_fields = ('name',)


class SubcategoryResource(BoundUserResourceMixin, resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')
    )

    class Meta:
        model = Subcategory
        fields = ('category', 'name')
        import_id_fields = ('category', 'name')


class AmortizationScheduleResource(BoundUserResourceMixin, resources.ModelResource):
    class Meta:
        model = AmortizationSchedule
        fields = (
            'next_payment_date', 'payment_amount', 'interest', 
            'capital_rate', 'capital_due_end_period', 'group_life_insurance_premium'
        )
        import_id_fields = ('next_payment_date',)


class AccountResource(BoundUserResourceMixin, resources.ModelResource):
    currency = fields.Field(
        column_name='currency',
        attribute='currency',
        widget=ForeignKeyWidget(Currency, 'code')
    )

    class Meta:
        model = Account
        fields = ('bank', 'iban_account', 'alias', 'currency')
        import_id_fields = ('iban_account',)
        export_order = ('bank', 'iban_account', 'alias', 'currency')


class AccountTransactionResource(resources.ModelResource):
    transaction_date = fields.Field(attribute='transaction_date', column_name='date')
    transaction_details = fields.Field(attribute='transaction_details', column_name='details')
    debit = fields.Field(attribute='debit', column_name='debit', default=0)
    credit = fields.Field(attribute='credit', column_name='credit', default=0)
    bank_account = fields.Field(
        attribute='bank_account', 
        column_name='bank_account_id', 
        widget=widgets.ForeignKeyWidget(Account, 'id')
    )

    class Meta:
        model = AccountTransaction
        fields = ('bank_account', 'transaction_date', 'transaction_details', 'debit', 'credit')
        import_id_fields = ('transaction_date', 'transaction_details', 'debit', 'credit')
