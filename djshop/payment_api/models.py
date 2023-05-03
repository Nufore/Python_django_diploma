from django.db import models


class PaymentTransactions(models.Model):
    order_id = models.IntegerField(null=False)
    account = models.IntegerField(null=False)
    summ = models.FloatField(null=False)
    satisfied = models.BooleanField(default=False)
