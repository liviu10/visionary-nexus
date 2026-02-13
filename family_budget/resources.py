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

    def _extract_iban_from_filename(self, filename):
        """Extract IBAN from the uploaded filename and look up the Account ID."""
        match = re.search(r'(RO\d{2}[A-Z]{4}\d+)', filename)
        if not match:
            raise ValueError(f"Could not extract IBAN from filename: {filename}")
        iban = match.group(1)
        try:
            account = Account.objects.get(iban_account=iban)
            return account.id
        except Account.DoesNotExist:
            raise ValueError(f"No account found for IBAN: {iban}")

    # Patterns to skip: page headers, page footers, and balance lines
    SKIP_PATTERNS = [
        'Titular cont:',
        'Roxana Petria',
        'Alexandra Ilie',
        'Şef Serviciu',
        'ING Bank N.V.',
        'Sucursala',
        'Sold ',
    ]
    SKIP_HEADERS = [
        'Data',
        'Detalii tranzactie',
    ]

    def _is_skip_row(self, row):
        """Return True if this row is a page header, footer, or balance line."""
        first_col = row[0].strip() if row[0] else ""
        second_col = row[1].strip() if len(row) > 1 and row[1] else ""
        # Check first column
        for pattern in self.SKIP_PATTERNS:
            if first_col.startswith(pattern):
                return True
        # Check second column (e.g. ",Roxana Petria")
        for pattern in self.SKIP_PATTERNS:
            if second_col.startswith(pattern):
                return True
        # Check third column for ING Bank / Sucursala lines
        third_col = row[2].strip() if len(row) > 2 and row[2] else ""
        for pattern in self.SKIP_PATTERNS:
            if third_col.startswith(pattern):
                return True
        return False

    @staticmethod
    def _is_column_header(row):
        """Return True if this is a column header row (e.g. ',Data,...,Debit,...')."""
        for val in row:
            if val and val.strip() in ('Debit', 'Credit', 'Detalii tranzactie'):
                return True
        return False

    @staticmethod
    def _find_first_detail(row, start=1):
        """Find the first non-empty text column after the given start index."""
        for i in range(start, len(row)):
            val = row[i].strip() if row[i] else ""
            if val:
                return val
        return ""

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        """Transform the raw ING bank statement CSV into a clean dataset."""
        # Resolve the bank account ID from the uploaded filename
        import_filename = kwargs.get('import_filename', '')
        bank_account_id = self._extract_iban_from_filename(import_filename)

        new_data = []
        current_transaction = None

        # Default column positions (header positions minus 1)
        debit_col = 6
        credit_col = 8

        for row in dataset:
            # Detect column header rows and update layout
            if self._is_column_header(row):
                for i, val in enumerate(row):
                    v = val.strip() if val else ""
                    if v == 'Debit':
                        debit_col = i - 1
                    elif v == 'Credit':
                        credit_col = i - 1
                continue

            # Skip page headers, footers, and balance lines
            if self._is_skip_row(row):
                continue

            first_col = row[0].strip() if row[0] else ""
            detail_text = self._find_first_detail(row)

            # Skip rows without useful data
            if not first_col and not detail_text:
                continue

            # Detect a date line (starts a new transaction)
            is_date_line = any(month in first_col for month in self.RO_MONTHS)

            if is_date_line:
                if current_transaction:
                    new_data.append(current_transaction)

                # Parse Romanian date "01 martie 2024" -> "2024-03-01"
                try:
                    day, month_name, year = first_col.split()
                    month = self.RO_MONTHS[month_name.lower()]
                    formatted_date = f"{year}-{month}-{day.zfill(2)}"
                except (ValueError, KeyError):
                    logger.warning(f"Could not parse date from: {first_col}")
                    current_transaction = None
                    continue

                debit_str = row[debit_col] if len(row) > debit_col else ""
                credit_str = row[credit_col] if len(row) > credit_col else ""

                current_transaction = {
                    'transaction_date': formatted_date,
                    'transaction_details': '',
                    'debit': self._parse_amount(debit_str),
                    'credit': self._parse_amount(credit_str),
                    'bank_account': bank_account_id,
                }
            else:
                # Continuation line — append extra details
                if current_transaction and detail_text:
                    sep = ' | ' if current_transaction['transaction_details'] else ''
                    current_transaction['transaction_details'] += sep + detail_text

        if current_transaction:
            new_data.append(current_transaction)

        # Replace the dataset with the cleaned data
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

    @staticmethod
    def _parse_amount(amount_str):
        """Parse Romanian-formatted amount '1.234,56' -> '1234.56' (2 decimal places)."""
        if not amount_str:
            return '0.00'
        clean_str = amount_str.replace('.', '').replace(',', '.')
        try:
            return f"{float(clean_str):.2f}"
        except ValueError:
            return '0.00'
