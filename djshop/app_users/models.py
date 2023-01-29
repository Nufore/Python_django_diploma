from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    account_balance = models.FloatField(default=0.0, null=False)
    avatar = models.ImageField(default=None, null=True, upload_to='avatars/')
