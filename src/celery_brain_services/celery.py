from __future__ import absolute_import

from celery import Celery

from . import celery_config
from .tasks.train_and_select_pipelines import train_and_select_pipelines

app = Celery('tasks')
app.config_from_object(celery_config)
CELERY_TIMEZONE = 'Europe/Madrid'
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(name='task_train_and_select_pipelines')
def task_train_and_select_pipelines():
    train_and_select_pipelines()
