from django.contrib import admin
from django.db.models import Sum
from import_export.admin import ImportExportModelAdmin
from .models import Category, Subcategory, Account, Transaction, AmortizationSchedule, Currency
from .resources import BankIngResource


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'currency', 'country')
    search_fields = ('code', 'currency')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'id')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category', 'name')
    list_select_related = ('category',)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('alias', 'bank', 'iban_account', 'currency', 'get_balance', 'user')
    list_filter = ('bank', 'user', 'currency')
    search_fields = ('bank', 'iban_account', 'alias')
    list_select_related = ('user', 'currency')

    @admin.display(description='Current Balance')
    def get_balance(self, obj):
        stats = obj.account_transactions.aggregate(
            d=Sum('debit'), c=Sum('credit')
        )
        balance = (stats['c'] or 0) - (stats['d'] or 0)
        return f"{balance:,.2f} {obj.currency.code}"


@admin.register(Transaction)
class TransactionAdmin(ImportExportModelAdmin):
    resource_classes = [BankIngResource]
    list_display = (
        'transaction_date', 'bank_account', 'category', 
        'subcategory', 'get_amount', 'transaction_details'
    )
    list_filter = ('transaction_date', 'category', 'bank_account', 'subcategory')
    search_fields = ('transaction_details',)
    list_select_related = ('bank_account', 'category', 'subcategory', 'bank_account__currency')

    @admin.display(description='Amount', ordering='debit')
    def get_amount(self, obj):
        if obj.debit > 0:
            return f"-{obj.debit}"
        return f"+{obj.credit}"

    fieldsets = (
        ('General Information', {
            'fields': ('bank_account', 'transaction_date', 'transaction_details')
        }),
        ('Categorization', {
            'fields': ('category', 'subcategory')
        }),
        ('Amounts', {
            'fields': ('debit', 'credit')
        }),
    )


@admin.register(AmortizationSchedule)
class AmortizationScheduleAdmin(ImportExportModelAdmin):
    list_display = (
        'next_payment_date', 'payment_amount', 'interest', 
        'capital_rate', 'capital_due_end_period', 'group_life_insurance_premium'
    )
    list_filter = ('next_payment_date',)
    search_fields = ('next_payment_date',)
    ordering = ('next_payment_date',)

    fieldsets = (
        ('Schedule Detail', {
            'fields': ('next_payment_date', 'payment_amount')
        }),
        ('Financial Detail', {
            'fields': ('interest', 'capital_rate', 'capital_due_end_period')
        }),
        ('Others', {
            'fields': ('group_life_insurance_premium',)
        }),
    )