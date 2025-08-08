from django.shortcuts import render
from django.views import View
from .models import Budget

# List all budgets for the user
class BudgetsListView(View):
    def get(self,request):
        context = {}
        budgets = Budget.objects.filter(user=request.user)
        context['budgets'] = budgets
        return render(request,'budgets/budgets_ls.html',context=context)

# Create a new budget for the user
class BudgetsCreateView(View):
    pass

# Update an existing budget for the user
class BudgetsUpdateView(View):
    pass

# Delete a budget for the user
class BudgetsDeleteView(View):
    pass