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
    RO_MONTHS = {
        'ianuarie': '01', 'februarie': '02', 'martie': '03', 'aprilie': '04',
        'mai': '05', 'iunie': '06', 'iulie': '07', 'august': '08',
        'septembrie': '09', 'octombrie': '10', 'noiembrie': '11', 'decembrie': '12',
    }

    SKIP_PATTERNS = [
        'Titular cont:', 'Roxana Petria', 'Alexandra Ilie',
        'Şef Serviciu', 'ING Bank N.V.', 'Sucursala', 'Sold ',
    ]

    transaction_date = fields.Field(attribute='transaction_date', column_name='date')
    transaction_details = fields.Field(attribute='transaction_details', column_name='details')
    debit = fields.Field(attribute='debit', column_name='debit', default=0)
    credit = fields.Field(attribute='credit', column_name='credit', default=0)
    bank_account = fields.Field(
        attribute='bank_account',
        column_name='bank_account_id',
        widget=widgets.ForeignKeyWidget(Account, 'id'),
    )

    class Meta:
        model = AccountTransaction
        fields = ('bank_account', 'transaction_date', 'transaction_details', 'debit', 'credit')
        import_id_fields = ('transaction_date', 'transaction_details', 'debit', 'credit')

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        import_filename = kwargs.get('import_filename', '')
        bank_account_id = self._extract_iban_from_filename(import_filename)

        new_data = []
        current_transaction = None
        debit_col = 6
        credit_col = 8

        for row in dataset:
            if self._is_column_header(row):
                for i, val in enumerate(row):
                    v = str(val).strip() if val else ""
                    if v == 'Debit': debit_col = i - 1
                    elif v == 'Credit': credit_col = i - 1
                continue

            if self._is_skip_row(row):
                continue

            first_col = str(row[0]).strip() if row[0] else ""
            detail_text = self._find_first_detail(row)

            is_date_line = any(month in first_col.lower() for month in self.RO_MONTHS)

            if is_date_line:
                if current_transaction:
                    # Validăm detaliile înainte de a salva tranzacția anterioară
                    if not current_transaction['transaction_details'].strip():
                        current_transaction['transaction_details'] = "-"
                    new_data.append(current_transaction)

                formatted_date = self._parse_romanian_date(first_col)
                if not formatted_date:
                    current_transaction = None
                    continue

                d_raw = row[debit_col] if len(row) > debit_col else ""
                c_raw = row[credit_col] if len(row) > credit_col else ""

                current_transaction = {
                    'transaction_date': formatted_date,
                    'transaction_details': detail_text if detail_text else "",
                    'debit': self._parse_amount(d_raw),
                    'credit': self._parse_amount(c_raw),
                    'bank_account': bank_account_id,
                }
            else:
                if current_transaction and detail_text:
                    sep = ' | ' if current_transaction['transaction_details'] else ''
                    current_transaction['transaction_details'] += sep + detail_text

        if current_transaction:
            if not current_transaction['transaction_details'].strip():
                current_transaction['transaction_details'] = "-"
            new_data.append(current_transaction)

        self._rebuild_dataset(dataset, new_data)

    def _extract_iban_from_filename(self, filename):
        match = re.search(r'(RO\d{2}[A-Z]{4}\d+)', filename)
        if not match:
            raise ValueError(f"Could not extract IBAN from filename: {filename}")
        iban = match.group(1)
        try:
            return Account.objects.get(iban_account=iban).id
        except Account.DoesNotExist:
            raise ValueError(f"No account found for IBAN: {iban}")

    def _is_skip_row(self, row):
        row_str = " ".join([str(cell) for cell in row[:3] if cell])
        return any(pattern in row_str for pattern in self.SKIP_PATTERNS)

    def _parse_romanian_date(self, date_str):
        try:
            parts = date_str.split()
            day, month_name, year = parts[0], parts[1].lower(), parts[2]
            return f"{year}-{self.RO_MONTHS[month_name]}-{day.zfill(2)}"
        except (IndexError, KeyError, ValueError):
            return None

    @staticmethod
    def _is_column_header(row):
        header_keys = ('Debit', 'Credit', 'Detalii tranzactie')
        return any(str(val).strip() in header_keys for val in row if val)

    @staticmethod
    def _find_first_detail(row, start=1):
        for i in range(start, len(row)):
            val = str(row[i]).strip() if row[i] else ""
            if val: return val
        return ""

    @staticmethod
    def _parse_amount(amount_str):
        if not amount_str: return '0.00'
        clean_str = str(amount_str).replace('.', '').replace(',', '.')
        try:
            return f"{float(clean_str):.2f}"
        except ValueError:
            return '0.00'

    @staticmethod
    def _rebuild_dataset(dataset, new_data):
        dataset.wipe()
        dataset.headers = ['date', 'details', 'debit', 'credit', 'bank_account_id']
        for item in new_data:
            dataset.append([
                item['transaction_date'],
                item['transaction_details'],
                item['debit'],
                item['credit'],
                item['bank_account'],
            ])
