from django.contrib.auth.models import User
from django.db import models

from categories.models import Category


class Budget(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category  = models.ForeignKey(Category, on_delete=models.CASCADE,blank=False,null=False)
    amount = models.DecimalField(decimal_places=2, max_digits=10,blank=False,null=False)
    month = models.PositiveSmallIntegerField()  # 1-12 for months
    year = models.PositiveIntegerField()        # e.g. 2025

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'month', 'year'], name='unique_user_month_year')
        ]
