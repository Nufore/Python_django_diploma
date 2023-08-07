from django.conf import settings
from store_api.models import PaymentStatus, Payment


def payment_attempt():
    payment = Payment.objects.filter(status_id=2,
                                     card_number__isnull=False,
                                     error_message__isnull=True).order_by('id').first()
    if payment is not None:
        if int(payment.card_number) % 2 == 0 and int(payment.card_number[-1]) != 0:
            status = PaymentStatus.objects.get(id=3)
            payment.status = status
            payment.error_message = None
            payment.save()
            print(f'Транзакция {payment.id} оплачена')
        elif int(payment.card_number) % 2 == 1 or int(payment.card_number[-1]) == 0:
            payment.error_message = 'Номер нечетный или заказчивается на 0.'
            payment.save()
            print(f'Транзакция {payment.id} не оплачена')
    else:
        print('Транзакций на оплату не найдено')
