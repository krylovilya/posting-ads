import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery("celery_django")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'main.send_digest_task',
        # 'schedule': crontab(day_of_week=0),
        'schedule': crontab(day_of_week=0),
    },
}
