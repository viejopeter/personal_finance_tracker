from django.urls import path

from transactions.views import TransactionsClassView

app_name = 'transactions'

urlpatterns = [
    path('',TransactionsClassView.as_view(), name='transactions'),
]