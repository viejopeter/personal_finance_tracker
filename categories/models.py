from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):

    INCOME = "Income"
    EXPENSE = "Expense"
    category_type_options = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]
    category = models.CharField(max_length=50)
    category_type = models.CharField(max_length=20, choices=category_type_options, default=INCOME)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.category
