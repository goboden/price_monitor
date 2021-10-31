from backend.update_prices import update_urls
from celery import Celery
from celery.schedules import crontab

celery_app = Celery('tasks', broker='redis://localhost:6379/0')


@celery_app.task
def update_urls_task():
    return update_urls()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=0, hour='*/1'), update_urls_task.s())
#	sender.add_periodic_task(crontab(minute='*/5'), update_urls_task.s())
