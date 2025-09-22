from django.urls import path
from budgets.views import  BudgetsListView,BudgetsCreateView,BudgetsUpdateView,BudgetsDeleteView

app_name='budgets'

urlpatterns = [
    path('',BudgetsListView.as_view(),name='budget_ls'),
    path('create/',BudgetsCreateView.as_view(),name='budget_create'),
    path('update/<int:pk>',BudgetsUpdateView.as_view(),name='budget_update'),
    path('delete/<int:pk>',BudgetsDeleteView.as_view(),name='budget_delete'),
]