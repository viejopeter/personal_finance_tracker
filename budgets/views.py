from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Budget, Category
from django import forms
from django.contrib import messages

# List all budgets for the user
class BudgetsListView(View):
    def get(self,request):
        context = {}
        budgets = Budget.objects.filter(user=request.user).order_by("year","month","category")
        context['budgets'] = budgets
        return render(request,'budgets/budgets_ls.html',context=context)

# Form
class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["category","amount","month","year",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select One"

# Create a new budget for the user
class BudgetsCreateView(View):
    def get(self,request):
        form = BudgetForm()
        form.fields['category'].queryset = Category.objects.filter(user=request.user,category_type='expense').order_by("category")
        return render(request, "budgets/budget_form.html", {"form": form, "action": "Create"})

    def post(self,request):
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget created Successfully!')
            return redirect("budgets:budget_ls")
        return render(request, "budgets/budget_form.html", {"form": form, "action": "Create"})

# Update an existing budget for the user
class BudgetsUpdateView(View):
    def get(self, request, pk):
        budget = Budget.objects.get(pk=pk, user=request.user)
        form = BudgetForm(instance=budget)
        return render(request, "budgets/budget_form.html", {"form": form, "budget": budget, "action": "Update"})

    def post(self, request, pk):
        budget = Budget.objects.get(pk=pk, user=request.user)
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated Successfully!')
            return redirect("budgets:budget_ls")
        return render(request, "budgets/budget_form.html", {"form": form, "budget": budget, "action": "Update"})

# Delete a budget for the user
class BudgetsDeleteView(View):

    def post(self, request, pk):
        budget = get_object_or_404(Budget, pk=pk)
        budget.delete()
        messages.success(request, 'Budget deleted successfully!')
        return redirect("budgets:budget_ls")