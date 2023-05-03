from django.apps import AppConfig


class PaymentApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment_api'

    def ready(self):
        from .jobs import updater
        updater.start()
