from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import payment_attempt


def start_scheduler():
    """
    Запуск джоба payment_attempt
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(payment_attempt, 'interval', seconds=10)
    scheduler.start()
