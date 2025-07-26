from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

#UserExtend model
class UserExtend(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    currency = models.CharField(max_length=50)
    monthly_budget_limit = models.DecimalField(decimal_places=2, max_digits=10)
    profile_picture = models.ImageField(upload_to="profile_pictures", null=True, blank=True)