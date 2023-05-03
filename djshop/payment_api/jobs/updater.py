from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import payment_attempt_f


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(payment_attempt_f, 'interval', seconds=10)
    scheduler.start()
