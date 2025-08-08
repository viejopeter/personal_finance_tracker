from django.urls import path
from budgets.views import  BudgetsListView,BudgetsCreateView,BudgetsUpdateView,BudgetsDeleteView

app_name='budgets'

urlpatterns = [
    path('',BudgetsListView.as_view(),name='budget_ls'),
    path('create/',BudgetsCreateView.as_view(),name='budget_create'),
    path('update/<int:id_budget>',BudgetsUpdateView.as_view(),name='budget_update'),
    path('delete/<int:id_budget>',BudgetsDeleteView.as_view(),name='budget_delete'),
]