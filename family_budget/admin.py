import csv
import io
import inspect

from django.contrib import admin
from django.db import models
from django.db.models import Sum
from django.utils.safestring import mark_safe
from django.forms import Textarea, TextInput, NumberInput, Select
from django.shortcuts import render
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from django.core.paginator import Paginator
from django.urls import reverse

from .models import (
    Account,
    AccountTransaction,
    AmortizationSchedule,
    Category,
    Currency,
    Subcategory
)
from .resources import (
    AccountResource,
    AccountTransactionResource,
    AmortizationScheduleResource,
    CategoryResource,
    CurrencyResource,
    SubcategoryResource
)


class UserImportMixin:
    exclude = ('user',)

    def get_resource_kwargs(self, request, *args, **kwargs):
        kwargs = super().get_resource_kwargs(request, *args, **kwargs)
        kwargs.update({"user": request.user})
        return kwargs

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Currency)
class CurrencyAdmin(UserImportMixin, admin.ModelAdmin):
    def get_actions(self, request):
        actions = super().get_queryset(request)
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request): return False

    def has_change_permission(self, request, obj=None): return False
    
    def has_delete_permission(self, request, obj=None): return False

    resource_classes = [CurrencyResource]
    list_display = ('id', 'code', 'currency', 'country',)
    list_display_links = None
    list_per_page = 20
    search_fields = ('code', 'currency', 'country',)
    ordering = ('id',)


@admin.register(Category)
class CategoryAdmin(UserImportMixin, admin.ModelAdmin):
    def get_actions(self, request):
        actions = super().get_queryset(request)
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request): return False

    def has_delete_permission(self, request, obj=None): return False

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('subcategories')

    @admin.display(description='Subcategories')
    def display_subcategories(self, obj):
        subcategories = obj.subcategories.all().values_list('name', flat=True)

        html_badges = [
            format_html(
                '<span style="background: #f0f0f0; color: #444; padding: 2px 10px; '
                'border-radius: 4px; font-size: 0.85em; margin: 2px; display: inline-block; '
                'border: 1px solid #ddd; font-weight: 600; font-family: sans-serif;">{}</span>',
                name
            )
            for name in subcategories
        ]
        
        return format_html('<div style="display: flex; flex-wrap: wrap; gap: 4px;">{}</div>', 
                           format_html("".join(html_badges)))

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 100%; max-width: 100%;'})},
    }

    resource_classes = [CategoryResource]
    list_display = ('id', 'name', 'display_subcategories',)
    list_display_links = ('name',)
    list_per_page = 20
    readonly_fields = ('display_subcategories',)
    search_fields = ('name', 'subcategories__name')
    ordering = ('id', 'name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

    def has_module_permission(self, request):
        return False


@admin.register(Account)
class AccountAdmin(UserImportMixin, ImportExportModelAdmin):
    resource_classes = [AccountResource]
    autocomplete_fields = ('currency',)
    list_display = ('alias', 'bank', 'iban_account', 'currency', 'get_balance', 'graph_button_field')
    list_per_page = 20
    list_filter = ('bank', 'currency',)
    search_fields = ('bank', 'iban_account', 'alias',)
    list_select_related = ('currency',)

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width: 100%; max-width: 100%;'})},
        models.DecimalField: {'widget': NumberInput(attrs={'style': 'width: 100%; max-width: 100%;'})},
    }

    readonly_fields = ('get_balance', 'display_transactions_table', 'graph_button_field')

    fieldsets = (
        ('General Information', {
            'fields': ('bank', 'iban_account', 'alias', 'currency', 'initial_balance', 'get_balance', 'graph_button_field')
        }),
        ('Transaction History', {
            'fields': ('display_transactions_table',),
        }),
    )

    @admin.display(description='Actions')
    def graph_button_field(self, obj):
        if not obj.pk:
            return "-"
        url = reverse('account_chart_view', args=[obj.pk])
        return mark_safe(f'<a href="{url}" class="button" style="background: #417690; color: white !important; padding: 5px 15px; vertical-align: middle;">📊 Chart</a>')

    @admin.display(description='Current Balance')
    def get_balance(self, obj):
        stats = obj.account_transactions.aggregate(
            d=Sum('debit'), c=Sum('credit')
        )
        balance = (obj.initial_balance or 0) + (stats['c'] or 0) - (stats['d'] or 0)
        return f"{balance:,.2f} {obj.currency.code}"

    @admin.display(description='')
    def display_transactions_table(self, obj):
        if not obj.pk:
            return mark_safe('<p style="padding:10px; color:#000;">Save the account to view transaction history.</p>')

        queryset = obj.account_transactions.all().select_related('category', 'subcategory').order_by('-transaction_date')
        app_label = queryset.model._meta.app_label
        model_name = queryset.model._meta.model_name
        graph_url = reverse('account_chart_view', args=[obj.pk])

        html = f"""
        <style>
            .field-display_transactions_table {{ display: block !important; }}
            .field-display_transactions_table > div {{ display: block !important; width: 100% !important; margin: 0 !important; padding: 0 !important; }}
            .field-display_transactions_table .control-label, .field-display_transactions_table label, .field-display_transactions_table .flex-container::before {{ display: none !important; }}
            .field-display_transactions_table .readonly {{ width: 100% !important; margin: 0 !important; padding: 0 !important; border: none !important; display: block !important; }}
            .tx-tools {{ display: flex; justify-content: space-between; align-items: center; padding: 10px; border: 1px solid #ccc; border-bottom: none; border-radius: 4px 4px 0 0; }}
            .tx-tools input {{ padding: 6px; width: 250px; border: 1px solid #ccc; border-radius: 3px; }}
            .btn-graph-inline {{ background: #79aec8; color: #000 !important; padding: 6px 12px; border-radius: 3px; text-decoration: none; font-weight: bold; font-size: 12px; }}
            .tx-wrapper {{ margin-bottom: 20px; border: 1px solid #ccc; border-radius: 0 0 4px 4px; }}
            .tx-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
            .tx-table th {{ padding: 12px 10px; text-align: left; border-bottom: 2px solid #ddd; color: #fff; cursor: pointer; position: relative; background: #417690; }}
            .tx-table th:after {{ content: ' ↕'; opacity: 0.3; }}
            .tx-table td {{ padding: 10px; border-bottom: 1px solid #eee; }}
            .tx-row {{ cursor: pointer; transition: background 0.2s; }}
            .tx-row:hover {{ background: #fff !important; color: #000; }}
            .tx-table tr.hidden {{ display: none !important; }}
            .amt {{ font-family: monospace; font-weight: bold; text-align: center; }}
            .debit {{ color: #dc3545; }}
            .credit {{ color: #198754; }}
            .badge-sub {{ background: #e0e0e0; padding: 2px 6px; border-radius: 10px; font-size: 11px; margin-left: 5px; color: #333; }}
            .tx-nav {{ padding: 15px; border-top: 1px solid #ddd; display: flex; justify-content: space-between; align-items: center; background: #f8f8f8; }}
            .tx-nav button {{ background: #79aec8; color: #000 !important; padding: 6px 14px; border-radius: 3px; border: 1px solid #5b8092; cursor: pointer; font-weight: bold; }}
            .tx-nav button:disabled {{ background: #ccc; border-color: #999; cursor: not-allowed; }}
            .current-page {{ font-weight: bold; color: #000; background: #fff; padding: 5px 10px; border: 1px solid #ccc; border-radius: 3px; }}
        </style>

        <div class="tx-tools">
            <input type="text" id="tx-search" placeholder="Search transactions..." onkeyup="filterTxTable()">
            <a href="{graph_url}" class="btn-graph-inline">📊 View Evolution Chart</a>
        </div>
        
        <div class="tx-wrapper">
            <table class="tx-table" id="transaction-table">
                <thead>
                    <tr>
                        <th style="width: 100px;" onclick="sortTxTable(0)">Date</th>
                        <th style="width: 40%;" onclick="sortTxTable(1)">Details</th>
                        <th onclick="sortTxTable(2)">Category</th>
                        <th style="width: 120px;" onclick="sortTxTable(3, true)">Debit</th>
                        <th style="width: 120px;" onclick="sortTxTable(4, true)">Credit</th>
                    </tr>
                </thead>
                <tbody id="tx-tbody">
        """

        for tx in queryset:
            sub = f'<span class="badge-sub">{tx.subcategory}</span>' if tx.subcategory else ""
            cat_text = f'{tx.category or "-"}{sub}'
            url = reverse(f'admin:{app_label}_{model_name}_change', args=[tx.pk])
            
            html += f"""
                <tr class="tx-row" onclick="window.location='{url}';">
                    <td data-value="{tx.transaction_date.isoformat()}">{tx.transaction_date.strftime('%d.%m.%Y')}</td>
                    <td>{tx.transaction_details}</td>
                    <td>{cat_text}</td>
                    <td class="amt debit" data-value="{tx.debit}">{"-" + f"{tx.debit:,.2f}" if tx.debit > 0 else ""}</td>
                    <td class="amt credit" data-value="{tx.credit}">{"+" + f"{tx.credit:,.2f}" if tx.credit > 0 else ""}</td>
                </tr>
            """

        html += """
                </tbody>
            </table>
            <div class="tx-nav">
                <div id="tx-counter" style="color: #000; font-size: 12px;"></div>
                <div>
                    <button type="button" id="tx-prev" onclick="changeTxPage(-1)">&laquo; Previous</button>
                    <span class="current-page" id="tx-info"></span>
                    <button type="button" id="tx-next" onclick="changeTxPage(1)">Next &raquo;</button>
                </div>
            </div>
        </div>

        <script>
            let currentTxPage = 1;
            const txPerPage = 15;
            let filteredRows = [];

            function initTxTable() {
                filteredRows = Array.from(document.querySelectorAll('.tx-row'));
                updateTxDisplay();
            }

            function filterTxTable() {
                const query = document.getElementById('tx-search').value.toLowerCase();
                const allRows = Array.from(document.querySelectorAll('.tx-row'));
                
                filteredRows = allRows.filter(row => {
                    const text = row.innerText.toLowerCase();
                    return text.includes(query);
                });

                allRows.forEach(row => row.classList.add('hidden'));
                currentTxPage = 1;
                updateTxDisplay();
            }

            function sortTxTable(colIdx, isNumeric = false) {
                const tbody = document.getElementById('tx-tbody');
                const rows = Array.from(tbody.querySelectorAll('.tx-row'));
                const isAsc = tbody.dataset.sortCol == colIdx && tbody.dataset.sortDir == 'asc';
                
                rows.sort((a, b) => {
                    let valA = a.cells[colIdx].getAttribute('data-value') || a.cells[colIdx].innerText;
                    let valB = b.cells[colIdx].getAttribute('data-value') || b.cells[colIdx].innerText;
                    
                    if(isNumeric) {
                        return isAsc ? parseFloat(valA) - parseFloat(valB) : parseFloat(valB) - parseFloat(valA);
                    }
                    return isAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
                });

                tbody.dataset.sortCol = colIdx;
                tbody.dataset.sortDir = isAsc ? 'desc' : 'asc';
                
                rows.forEach(row => tbody.appendChild(row));
                filterTxTable(); 
            }

            function updateTxDisplay() {
                const totalPages = Math.ceil(filteredRows.length / txPerPage) || 1;
                const start = (currentTxPage - 1) * txPerPage;
                const end = start + txPerPage;

                document.querySelectorAll('.tx-row').forEach(row => row.classList.add('hidden'));
                
                filteredRows.slice(start, end).forEach(row => {
                    row.classList.remove('hidden');
                });

                document.getElementById('tx-info').innerText = currentTxPage + ' / ' + totalPages;
                document.getElementById('tx-counter').innerText = 'Showing ' + filteredRows.length + ' transactions';
                document.getElementById('tx-prev').disabled = currentTxPage === 1;
                document.getElementById('tx-next').disabled = currentTxPage === totalPages;
            }

            function changeTxPage(step) {
                currentTxPage += step;
                updateTxDisplay();
            }

            document.addEventListener('DOMContentLoaded', initTxTable);
            if (document.readyState === "complete" || document.readyState === "interactive") {
                initTxTable();
            }
        </script>
        """
        return mark_safe(html)


@admin.register(AccountTransaction)
class AccountTransactionAdmin(ImportExportModelAdmin):
    resource_classes = [AccountTransactionResource]
    autocomplete_fields = ('bank_account', 'category', 'subcategory')

    def _get_cleaned_csv_file(self, import_file):
        raw_content = import_file.read()
        try:
            decoded_content = raw_content.decode('utf-8-sig')
        except UnicodeDecodeError:
            decoded_content = raw_content.decode('latin-1')
        
        lines = decoded_content.splitlines()
        reader = list(csv.reader(lines))
        
        if not reader: return None

        max_cols = max(len(row) for row in reader)
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        for row in reader:
            if len(row) < max_cols:
                row.extend([""] * (max_cols - len(row)))
            writer.writerow(row)
            
        new_content = output.getvalue().encode('utf-8')
        return io.BytesIO(new_content)

    def import_action(self, request, *args, **kwargs):
        if request.method == "POST" and "import_file" in request.FILES:
            import_file = request.FILES['import_file']
            cleaned_file = self._get_cleaned_csv_file(import_file)
            
            if cleaned_file:
                request.FILES['import_file'].file = cleaned_file
                request.FILES['import_file'].size = cleaned_file.getbuffer().nbytes

        return super().import_action(request, *args, **kwargs)

    def get_import_data_kwargs(self, request, *args, **kwargs):
        kw = super().get_import_data_kwargs(request, *args, **kwargs)
        form = kwargs.get('form')
        
        if form and hasattr(form, 'cleaned_data'):
            import_file = form.cleaned_data.get('import_file')
            if import_file:
                kw['import_filename'] = import_file.name
            else:
                original_file_name = form.cleaned_data.get('original_file_name', '')
                if original_file_name:
                    kw['import_filename'] = original_file_name
        return kw

    @admin.display(description='Amount', ordering='debit')
    def get_amount(self, obj):
        if obj.debit > 0:
            return f"-{obj.debit}"
        return f"+{obj.credit}"

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
        models.CharField: {'widget': Textarea(attrs={'rows': 3, 'cols': 40})},
    }
    list_display = (
        'transaction_date', 'bank_account', 'category', 
        'subcategory', 'get_amount', 'transaction_details'
    )
    list_filter = ('transaction_date', 'category', 'bank_account', 'subcategory')
    list_per_page = 20
    search_fields = ('transaction_details',)
    list_select_related = ('bank_account', 'category', 'subcategory', 'bank_account__currency')
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
