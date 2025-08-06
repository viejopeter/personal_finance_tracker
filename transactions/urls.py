from django.urls import path

from transactions.views import TransactionsListView, TransactionsCreateView

app_name = 'transactions'

urlpatterns = [
    path('',TransactionsListView.as_view(), name='transactions_ls'),
    path('create/',TransactionsCreateView.as_view(), name='transactions_create'),
]