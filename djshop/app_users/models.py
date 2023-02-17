from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fio = models.CharField(max_length=90)
    phone_number = models.CharField(max_length=20, unique=True)
    account_balance = models.FloatField(default=0.0, null=False)
    avatar = models.ImageField(default=None, null=True, upload_to='avatars/')

    def __str__(self):
        return f'{self.user.id}'
