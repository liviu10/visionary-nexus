from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .models import Category, Subcategory, Account, Transaction, AmortizationSchedule
from .resources import BankIngResource


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category', 'name')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('alias', 'bank', 'iban_account', 'user')
    list_filter = ('bank', 'user')
    search_fields = ('bank', 'iban_account', 'alias')
    ordering = ('alias', 'bank')


@admin.register(Transaction)
class TransactionAdmin(ImportExportModelAdmin):
    resource_classes = [BankIngResource]
    list_display = ('transaction_date', 'bank_account', 'category', 'subcategory', 'debit', 'credit', 'transaction_details')
    list_filter = ('transaction_date', 'category', 'bank_account', 'subcategory')
    search_fields = ('transaction_details',)
    ordering = ('-transaction_date',)

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
    list_display = ('next_payment_date', 'payment_amount', 'interest', 'capital_rate', 'capital_due_end_period', 'group_life_insurance_premium')
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
