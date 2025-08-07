from django.urls import path

from transactions.views import TransactionsListView, TransactionsCreateView, TransactionsUpdateView , TransactionsDeleteView

app_name = 'transactions'

urlpatterns = [
    path('',TransactionsListView.as_view(), name='transactions_ls'),
    path('create/',TransactionsCreateView.as_view(), name='transactions_create'),
    path('update/<int:id_transaction>',TransactionsUpdateView.as_view(), name='transactions_update'),

    path('delete/<int:id_transaction>',TransactionsDeleteView.as_view(),name='transactions_delete'),
]