from django.shortcuts import render
from django.views import View
from django.db.models import Q
from transactions.models import Transaction


class TransactionsClassView(View):
    def get(self, request):
        context = {}
        transactions = Transaction.objects.filter(
            Q(origin_account__user=request.user) | Q(destination_account__user=request.user)
        )
        context['transactions'] = transactions
        return render(request,'transactions/transactions_ls.html',context=context)


