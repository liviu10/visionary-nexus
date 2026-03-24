from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required
from .models import Account
import json


@staff_member_required
def account_chart_view(request, pk):
    account = get_object_or_404(Account, pk=pk)
    transactions = account.account_transactions.all().order_by('transaction_date')
    
    raw_data = []
    current_balance = float(account.initial_balance or 0)
    
    raw_data.append({
        'date': 'Start',
        'balance': current_balance,
        'category': None,
        'subcategory': None,
        'debit': 0,
        'credit': 0
    })
    
    for tx in transactions:
        current_balance += float(tx.credit or 0) - float(tx.debit or 0)
        raw_data.append({
            'date': tx.transaction_date.strftime('%d.%m.%Y'),
            'iso_date': tx.transaction_date.isoformat(),
            'balance': current_balance,
            'category': str(tx.category) if tx.category else "Uncategorized",
            'subcategory': str(tx.subcategory) if tx.subcategory else "No Subcategory",
            'debit': float(tx.debit or 0),
            'credit': float(tx.credit or 0)
        })
        
    context = {
        'account': account,
        'raw_data_json': json.dumps(raw_data),
    }
    return render(request, 'admin/account_chart.html', context)
