from django.db import models
from django.utils import timezone
from accounts.models import Account
from categories.models import Category


class Transaction(models.Model):

    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSFER = 'transfer'
    choices = (
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
        (TRANSFER, 'Transfer'),
    )

    origin_account = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, default=None,related_name='origin_account')
    destination_account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, default=None,related_name='destination_account')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, default=None)
    description = models.TextField(max_length=500, null=False, blank=False)
    amount = models.DecimalField(decimal_places=2, max_digits=10,null=False,blank=False)
    datetime = models.DateTimeField(null=False, blank=False,default=timezone.now)
    type = models.CharField(max_length=20, choices=choices, default=None,blank=False)

    def __str__(self):
        return f"Description: {self.description}, Amount: {self.amount}"
