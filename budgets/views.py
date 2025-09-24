from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Budget, Category
from transactions.models import Transaction
from django import forms
from django.contrib import messages
from django.db.models import Sum

# List all budgets for the user
class BudgetsListView(View):
    def get(self,request):
        budgets = Budget.objects.filter(user=request.user).order_by("year","month","category")
        comparisons = []
        for budget in budgets:
            spent = Transaction.objects.filter(
                category=budget.category,
                origin_account__user=request.user,
                datetime__year=budget.year,
                datetime__month=budget.month,
                type='expense'
            ).aggregate(total=Sum('amount'))['total'] or 0
            remaining = budget.amount - spent
            comparisons.append({
                'category': budget.category.category,
                'month': budget.month,
                'year': budget.year,
                'budget': budget.amount,
                'spent': spent,
                'remaining': remaining
            })
        return render(request,'budgets/budgets_ls.html',{'budgets': budgets, 'comparisons': comparisons})

# Form
class BudgetForm(forms.ModelForm):

    #Customized field for the form
    month_year = forms.CharField(
        label="Month and Year",
        widget=forms.TextInput(attrs={"type": "month"})
    )

    class Meta:
        model = Budget
        fields = ["category","amount"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select One"

    def clean(self):
        cleaned_data = super().clean()
        month_year = cleaned_data.get("month_year")
        if month_year:
            try:
                year, month = map(int, month_year.split("-"))
                cleaned_data["month"] = month
                cleaned_data["year"] = year
            except Exception:
                self.add_error("month_year", "Invalid month/year format.")
        return cleaned_data


# Create a new budget for the user
class BudgetsCreateView(View):
    def get(self,request):
        form = BudgetForm()
        form.fields['category'].queryset = Category.objects.filter(user=request.user,category_type='expense').order_by("category")
        return render(request, "budgets/budget_form.html", {"form": form, "action": "Create"})

    def post(self,request):
        form = BudgetForm(request.POST)
        form.fields['category'].queryset = Category.objects.filter(user=request.user,category_type='expense').order_by("category")
        if form.is_valid():
            budget = form.save(commit=False)
            cleaned = form.cleaned_data
            budget.month = cleaned.get("month")
            budget.year = cleaned.get("year")
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
        form.fields['category'].queryset = Category.objects.filter(user=request.user,category_type='expense').order_by("category")
        return render(request, "budgets/budget_form.html", {"form": form, "budget": budget, "action": "Update"})

    def post(self, request, pk):
        budget = Budget.objects.get(pk=pk, user=request.user)
        form = BudgetForm(request.POST, instance=budget)
        form.fields['category'].queryset = Category.objects.filter(user=request.user,category_type='expense').order_by("category")
        if form.is_valid():
            cleaned = form.cleaned_data
            budget.month = cleaned.get("month")
            budget.year = cleaned.get("year")
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
