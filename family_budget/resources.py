import os
import logging
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Transaction, Category, Subcategory, Account

# Privacy-focused configuration: Force offline mode for transformers
os.environ["TRANSFORMERS_OFFLINE"] = "1"

logger = logging.getLogger(__name__)

class BaseTransactionResource(resources.ModelResource):
    """Base resource for transaction imports with local ML fallback."""
    
    bank_account = fields.Field(
        column_name='bank_account',
        attribute='bank_account',
        widget=ForeignKeyWidget(Account, 'iban_account')
    )
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')
    )
    subcategory = fields.Field(
        column_name='subcategory',
        attribute='subcategory',
        widget=ForeignKeyWidget(Subcategory, 'name')
    )

    KEYWORD_FLAGS = {} # To be overridden by subclasses

    class Meta:
        model = Transaction
        fields = ('id', 'bank_account', 'transaction_date', 'transaction_details', 'debit', 'credit', 'category', 'subcategory')
        export_order = fields
        skip_unchanged = True
        report_skipped = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classifier = None
        self._initialize_ml()

    def _initialize_ml(self):
        """Initialize the local ML classifier lazily and safely."""
        try:
            from transformers import pipeline
            self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
            logger.info(f"{self.__class__.__name__}: Local ML classifier initialized.")
        except Exception as e:
            logger.warning(f"ML Processing disabled: {str(e)}.")

    def _match_keywords(self, text):
        """Try to match keywords in transaction details."""
        if not text:
            return None, None
            
        text_upper = text.upper()
        for keyword, mapping in self.KEYWORD_FLAGS.items():
            if keyword in text_upper:
                return mapping
        return None, None

    def before_import_row(self, row, **kwargs):
        """
        Logic hierarchy:
        1. Exact Keyword Flags (Bank-Specific)
        2. Local ML Fallback (SMART)
        """
        details = row.get('transaction_details')
        if not details:
            return

        # 1. Keyword-Based Flags
        cat_name, subcat_name = self._match_keywords(details)
        if cat_name:
            row['category'] = cat_name
            if subcat_name:
                row['subcategory'] = subcat_name
            return

        # 2. Local ML Fallback
        if self.classifier and not row.get('category'):
            try:
                labels = list(Category.objects.values_list('name', flat=True))
                if labels:
                    result = self.classifier(details, labels)
                    row['category'] = result['labels'][0]
            except Exception as e:
                logger.error(f"ML Error: {str(e)}")

    def get_import_id_fields(self):
        return ['transaction_date', 'transaction_details', 'debit', 'credit', 'bank_account']


class BankIngResource(BaseTransactionResource):
    """Specific resource for ING Bank statements."""
    KEYWORD_FLAGS = {
        "AMZ": ("Shopping", "Amazon"),
        "NETFLIX": ("Subscriptions", "Entertainment"),
        "GOOGLE": ("Services", "Digital"),
        "KFC": ("Food", "Restaurants"),
        "SHELL": ("Transport", "Fuel"),
    }
    
    class Meta(BaseTransactionResource.Meta):
        name = "ING Bank"
        model = Transaction
