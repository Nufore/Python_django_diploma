from django.apps import AppConfig


class PaymentSchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment_scheduler'

    def ready(self):
        """
        Запуск шедулера.
        """
        from .jobs import updater
        updater.start_scheduler()
