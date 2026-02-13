from django.contrib import admin
from django.db.models import Sum
from django.db import models
from django.forms import Textarea
from import_export.admin import ImportExportModelAdmin
from .models import Category, Subcategory, Account, AccountTransaction, AmortizationSchedule, Currency
from .resources import (
    CurrencyResource, CategoryResource, 
    SubcategoryResource, AccountResource, AmortizationScheduleResource, AccountTransactionResource
)
from .formats import INGPDF


class UserImportMixin:
    def get_resource_kwargs(self, request, *args, **kwargs):
        kwargs = super().get_resource_kwargs(request, *args, **kwargs)
        kwargs.update({"user": request.user})
        return kwargs

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Currency)
class CurrencyAdmin(UserImportMixin, ImportExportModelAdmin):
    resource_classes = [CurrencyResource]
    list_display = ('code', 'currency', 'country')
    search_fields = ('code', 'currency')


@admin.register(Category)
class CategoryAdmin(UserImportMixin, ImportExportModelAdmin):
    resource_classes = [CategoryResource]
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Subcategory)
class SubcategoryAdmin(UserImportMixin, ImportExportModelAdmin):
    resource_classes = [SubcategoryResource]
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category', 'name')
    list_select_related = ('category',)


class AccountTransactionInline(admin.TabularInline):
    model = AccountTransaction
    extra = 0
    fields = ('category', 'subcategory', 'get_date_formatted', 'transaction_details', 'debit', 'credit')
    readonly_fields = ('get_date_formatted', 'transaction_details', 'debit', 'credit')
    show_change_link = True
    can_delete = False
    ordering = ('-transaction_date',)
    
    @admin.display(description='Inregistrat')
    def get_date_formatted(self, obj):
        return obj.transaction_date.strftime("%d.%m.%Y")
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category', 'subcategory').order_by('-transaction_date')


@admin.register(Account)
class AccountAdmin(UserImportMixin, ImportExportModelAdmin):
    resource_classes = [AccountResource]
    inlines = [AccountTransactionInline]
    list_display = ('alias', 'bank', 'iban_account', 'currency', 'get_balance', 'user')
    list_filter = ('bank', 'user', 'currency')
    search_fields = ('bank', 'iban_account', 'alias')
    list_select_related = ('user', 'currency')

    @admin.display(description='Current Balance')
    def get_balance(self, obj):
        stats = obj.account_transactions.aggregate(
            d=Sum('debit'), c=Sum('credit')
        )
        balance = (obj.initial_balance or 0) + (stats['c'] or 0) - (stats['d'] or 0)
        return f"{balance:,.2f} {obj.currency.code}"


@admin.register(AccountTransaction)
class AccountTransactionAdmin(ImportExportModelAdmin):
    resource_classes = [AccountTransactionResource]
    formats = [INGPDF]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.CharField: {'widget': Textarea(attrs={'rows': 3, 'cols': 40})},
    }
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
class AmortizationScheduleAdmin(UserImportMixin, ImportExportModelAdmin):
    resource_classes = [AmortizationScheduleResource]
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