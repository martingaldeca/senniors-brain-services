from celery.schedules import crontab

beat_schedule = {
    'task_train_and_select_pipelines': {
        'task': 'celery_brain_services.celery.task_train_and_select_pipelines',
        'schedule': crontab(hour=5, minute=0)
    }
}
