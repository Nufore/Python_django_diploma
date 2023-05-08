from django.db import models


class PaymentTransactions(models.Model):
    order_id = models.IntegerField(null=False)
    account = models.IntegerField(null=True)
    summ = models.FloatField(null=True)
    satisfied = models.BooleanField(default=False)
