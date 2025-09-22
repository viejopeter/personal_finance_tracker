from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    icon = models.ImageField(upload_to="icon_accounts",null=True,blank=True)

    def __str__(self):
        return self.name
