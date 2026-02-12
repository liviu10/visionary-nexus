from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint, Q, CheckConstraint
from django.core.exceptions import ValidationError


class Currency(models.Model):
    country = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=3, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='currencies')

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.code


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='categories')
    
    class Meta:
        ordering = ('name',)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

    class Meta:
        ordering = ('category', 'name')
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"
        constraints = [
            UniqueConstraint(fields=['category', 'name'], name='unique_subcat_per_cat')
        ]

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Account(models.Model):
    bank = models.CharField(max_length=100)
    iban_account = models.CharField(max_length=34, unique=True)
    alias = models.CharField(max_length=100, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name='accounts')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accounts')

    def clean(self):
        if self.iban_account:
            self.iban_account = self.iban_account.replace(" ", "").upper()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.alias or self.bank} - {self.iban_account} ({self.currency.code})"


class Transaction(models.Model):
    bank_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_date = models.DateField()
    transaction_details = models.CharField(max_length=1000)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    class Meta:
        ordering = ('-transaction_date',)
        constraints = [
            CheckConstraint(
                condition=(Q(debit__gt=0) & Q(credit=0)) | (Q(credit__gt=0) & Q(debit=0)),
                name='debit_exclude_credit'
            ),
            CheckConstraint(
                condition=Q(debit__gte=0) & Q(credit__gte=0),
                name='no_negative_values'
            )
        ]

    def clean(self):
        super().clean()
        if self.category and self.subcategory:
            if self.subcategory.category != self.category:
                raise ValidationError({
                    'subcategory': f"Subcategoria '{self.subcategory.name}' nu aparține de '{self.category.name}'."
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class AmortizationSchedule(models.Model):
    next_payment_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest = models.DecimalField(max_digits=15, decimal_places=2)
    capital_rate = models.DecimalField(max_digits=15, decimal_places=2)
    capital_due_end_period = models.DecimalField(max_digits=15, decimal_places=2)
    group_life_insurance_premium = models.DecimalField(max_digits=15, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='amortization_schedules')

    class Meta:
        ordering = ('next_payment_date',)
        verbose_name = "Amortization schedule"
        verbose_name_plural = "Amortization schedules"
        indexes = [
            models.Index(fields=["next_payment_date"], name="as_pay_date_idx"),
        ]

    def __str__(self):
        return f"Payment {self.next_payment_date} - {self.payment_amount}"