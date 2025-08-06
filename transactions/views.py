from django.shortcuts import render
from django.views import View
from django.db.models import Q

from categories.models import Category
from transactions.models import Transaction
from accounts.models import Account


class TransactionsListView(View):
    def get(self, request):
        context = {}
        transactions = Transaction.objects.filter(
            Q(origin_account__user=request.user) | Q(destination_account__user=request.user)
        )
        context['transactions'] = transactions
        return render(request,'transactions/transactions_ls.html',context=context)

class TransactionsCreateView(View):
    def get(self, request):
        transaction_type = Transaction.choices
        categories_ls = Category.objects.filter(user=request.user).values('id','category')
        category_select = [(a['id'],a['category']) for a in categories_ls]
        accounts_ls = Account.objects.filter(user=request.user).values('id','name')
        accounts_select = [(a['id'],a['name']) for a in accounts_ls]
        context={
            'transaction_type': transaction_type,
            'accounts': accounts_select,
            'categories': category_select
        }
        return render(request,"transactions/transactions_form.html",context=context)



