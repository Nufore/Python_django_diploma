from .models import PaymentTransactions
from app_store.models import Order, PaymentStatus
import requests
import json


def payment_attempt():
    transaction = PaymentTransactions.objects.filter(satisfied=False).order_by('id').first()
    if transaction:
        response = requests.request('GET', 'http://127.0.0.1:8000/api/payment', params={'number': transaction.account})
        if response.json().get('success'):
            order = Order.objects.get(id=transaction.order_id)
            status = PaymentStatus.objects.get(id=1)
            order.payment.status = status
            order.save()
            transaction.satisfied = True
            print('1')
        print('2')
    print('3')

