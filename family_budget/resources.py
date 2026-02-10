import logging
import joblib
import numpy as np
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateWidget, DecimalWidget
from django.db.models import Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

from .models import Transaction, Category, Subcategory, Account

logger = logging.getLogger(__name__)

class SmartTransactionResource(resources.ModelResource):
    """
    Clasa de BAZĂ. Aici stă toată inteligența:
    1. Widget-uri pentru ForeignKeys (Cont, Categorie)
    2. Logica de antrenare ML (SGDClassifier)
    3. Logica de predicție
    """
    
    # Definim relațiile standard care sunt la fel peste tot
    bank_account = fields.Field(
        column_name='bank_account', # Va fi suprascris în subclase dacă e cazul
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

    class Meta:
        model = Transaction
        # Câmpurile care trebuie importate în DB
        fields = ('id', 'bank_account', 'transaction_date', 'transaction_details', 'debit', 'credit', 'category', 'subcategory')
        # Identificatori unici pentru a evita duplicatele
        import_id_fields = ['transaction_date', 'transaction_details', 'debit', 'credit']
        skip_unchanged = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_pipeline = None
        self._train_model_on_history()

    def _train_model_on_history(self):
        """Logica de antrenare automată la inițializare."""
        # Luăm istoricul clasificat
        history = Transaction.objects.filter(category__isnull=False).values_list(
            'transaction_details', 'category__name', 'subcategory__name'
        )

        if len(history) < 5: # Minim 5 tranzacții ca să aibă sens
            return

        X_train = [h[0] for h in history]
        # Eticheta este combinată: "Categorie||Subcategorie"
        y_train = [f"{h[1]}||{h[2] if h[2] else ''}" for h in history]

        self.model_pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 3), min_df=1)),
            ('clf', SGDClassifier(loss='hinge', alpha=1e-3, max_iter=1000, random_state=42)),
        ])
        
        try:
            self.model_pipeline.fit(X_train, y_train)
        except Exception as e:
            logger.warning(f"ML Training skipped: {e}")

    def before_import_row(self, row, **kwargs):
        """Logica de predicție rulată pentru fiecare rând."""
        # 1. Obținem textul tranzacției (numele coloanei depinde de clasa copil)
        # 'transaction_details' este atributul intern al modelului Django
        # row-ul vine cu cheile din CSV (ex: 'Detalii' sau 'Description')
        
        # Aici e trucul: trebuie să găsim care câmp din row corespunde lui 'transaction_details'
        # Ne bazăm pe faptul că subclasa a mapat corect câmpul
        
        # Căutăm valoarea textului. Deoarece 'row' are cheile din CSV, trebuie să știm cum le-am mapat.
        # Simplificare: facem predicția doar dacă câmpul category e gol
        if row.get('category'):
            return

        # Căutăm textul brut. Din păcate, `before_import_row` primește `row` cu cheile din fișierul importat.
        # Trebuie să iterăm prin field-urile resursei pentru a găsi care e 'transaction_details'
        
        text_to_analyze = None
        for field in self.get_fields():
            if field.attribute == 'transaction_details':
                # Luăm numele coloanei din CSV definit în resursă
                column_name_in_csv = field.column_name
                text_to_analyze = row.get(column_name_in_csv)
                break
        
        if not text_to_analyze or not self.model_pipeline:
            return

        try:
            prediction = self.model_pipeline.predict([text_to_analyze])[0]
            parts = prediction.split('||')
            row['category'] = parts[0] # Setăm numele categoriei (ForeignKeyWidget îl va căuta)
            if len(parts) > 1 and parts[1]:
                row['subcategory'] = parts[1]
        except Exception:
            pass


class BankIngResource(SmartTransactionResource):
    """Resource dedicat ING - mapează coloanele specifice ING"""
    transaction_date = fields.Field(attribute='transaction_date', column_name='Data')
    transaction_details = fields.Field(attribute='transaction_details', column_name='Detalii tranzactie')
    debit = fields.Field(attribute='debit', column_name='Debit', widget=DecimalWidget())
    credit = fields.Field(attribute='credit', column_name='Credit', widget=DecimalWidget())
    
    class Meta(SmartTransactionResource.Meta):
        name = "Import ING (CSV/XLS)"
