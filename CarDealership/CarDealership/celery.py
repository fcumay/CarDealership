import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarDealership.settings')

app = Celery('CarDealership')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'buy_car': {
        'task': 'dealership.tasks.buy_car',
        'schedule': crontab(minute='*/10'),
    },
    'get_dealers': {
        'task': 'dealership.tasks.get_dealers',
        'schedule': crontab(minute='*/20'),
    },
}
