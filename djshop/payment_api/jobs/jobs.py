from django.conf import settings
from payment_api.models import PaymentTransactions
from app_store.models import Order, PaymentStatus
import requests
import json


def payment_attempt():
    transaction = PaymentTransactions.objects.filter(satisfied=False).order_by('id').first()
    if transaction is not None:
        response = requests.request('GET', 'http://127.0.0.1:8000/api/payment', params={'number': transaction.account})
        order = Order.objects.get(id=transaction.order_id)
        if response.json().get('success'):
            status = PaymentStatus.objects.get(id=1)
            order.payment.status = status
            order.payment.card_number = transaction.account
            order.payment.error_message = None
            order.payment.save()
            transaction.satisfied = True
            transaction.save()
            print(f'Транзакция {transaction.id} оплачена')
        else:
            order.payment.error_message = f'Номер нечетный или заказчивается на 0. {response.json().get("message")}'
            order.payment.save()
            print(f'Транзакция {transaction.id} не оплачена')
    else:
        print('Транзакций на оплату не найдено')



