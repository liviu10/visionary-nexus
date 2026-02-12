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
from .models import Transaction, Category, Subcategory, Account, Currency, AmortizationSchedule
import tablib
import re
from .models import Transaction


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


class TransactionResource(resources.ModelResource):
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
        model = Transaction
        fields = ('bank_account', 'transaction_date', 'transaction_details', 'debit', 'credit', 'user')
        import_id_fields = ('transaction_date', 'transaction_details', 'debit', 'credit')

    def before_import(self, dataset, using_transactions=True, dry_run=False, **kwargs):
        filename = kwargs.get('file_name', '')
        clean_filename = filename.replace(" ", "").upper()
        iban_match = re.search(r'RO\d{2}[A-Z]{4}[A-Z0-9]{16}', clean_filename)
        found_account_id = None
        if iban_match:
            iban = iban_match.group()
            try:
                acc = Account.objects.get(iban_account__iexact=iban)
                found_account_id = acc.id
            except Account.DoesNotExist:
                pass

        luni = {
            'ianuarie': '01', 'februarie': '02', 'martie': '03', 'aprilie': '04',
            'mai': '05', 'iunie': '06', 'iulie': '07', 'august': '08',
            'septembrie': '09', 'octombrie': '10', 'noiembrie': '11', 'decembrie': '12'
        }

        def parse_ing_date(val):
            if not val: return None
            val = str(val).lower().strip()
            match = re.search(r'(\d{1,2})\s+([a-zăîâşţșț]+)\s+(\d{4})', val)
            if match:
                day, month_str, year = match.groups()
                month_str = month_str.replace('ş', 's').replace('ș', 's').replace('ţ', 't').replace('ț', 't')
                mm = luni.get(month_str)
                if mm:
                    return f"{year}-{mm}-{day.zfill(2)}"
            return None

        def clean_ing_num(val):
            if not val or str(val).strip() in ['', 'nan', 'None']: return "0"
            clean = str(val).replace('"', '').replace('.', '').replace(',', '.')
            return clean if re.match(r'^-?\d+(\.\d+)?$', clean) else "0"

        new_rows = []
        current_transaction = None
        found_at_idx = 1 

        for row in dataset:
            r = [str(x).strip() if x is not None else "" for x in row]
            
            potential_date = None
            for i, cell in enumerate(r):
                d = parse_ing_date(cell)
                if d:
                    potential_date = d
                    found_at_idx = i
                    break
            
            if potential_date:
                if current_transaction:
                    new_rows.append(current_transaction)
                
                current_transaction = {
                    'date': potential_date,
                    'details': r[found_at_idx + 3] if len(r) > found_at_idx + 3 else "",
                    'debit': clean_ing_num(r[found_at_idx + 6] if len(r) > found_at_idx + 6 else "0"),
                    'credit': clean_ing_num(r[found_at_idx + 8] if len(r) > found_at_idx + 8 else "0"),
                    'bank_account_id': found_account_id
                }
            elif current_transaction:
                idx_detalii = found_at_idx + 3
                extra = r[idx_detalii] if len(r) > idx_detalii else ""
                if extra and not any(x in extra for x in ['Titular', 'Roxana', 'Şef', 'Pagina']):
                    current_transaction['details'] += f" | {extra}"

        if current_transaction:
            new_rows.append(current_transaction)

        dataset.wipe()
        dataset.headers = ['date', 'details', 'debit', 'credit', 'bank_account_id']
        for item in new_rows:
            dataset.append([
                item['date'], 
                item['details'], 
                item['debit'], 
                item['credit'], 
                item['bank_account_id']
            ])

        super().before_import(dataset, using_transactions=True, dry_run=False, **kwargs)
