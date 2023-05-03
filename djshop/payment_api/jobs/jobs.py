from django.conf import settings
from payment_api.models import PaymentTransactions
from app_store.models import Order, PaymentStatus
import requests
import json


def payment_attempt_f():
    transaction = PaymentTransactions.objects.filter(satisfied=False).order_by('id').first()
    if transaction is not None:
        print(transaction.account, transaction.order_id)
        response = requests.request('GET', 'http://127.0.0.1:8000/api/payment', params={'number': transaction.account})
        if response.json().get('success'):
            order = Order.objects.get(id=transaction.order_id)
            print('ORDER', order.payment.status)
            status = PaymentStatus.objects.get(id=1)
            print('STATUS', status)
            order.payment.status = status
            print('ORDER AFTER', order.payment.status)
            order.payment.save()
            transaction.satisfied = True
            transaction.save()
            print('Транзакция оплачена')
            return
        print('Транзакция не оплачена')
    print('Транзакций на оплату не найдено')



