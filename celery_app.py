# celery_app.py
from celery import Celery

app = Celery(
    'tasks',
    broker='pyamqp://guest@localhost//',
    backend='rpc://'
)
import celery_task
