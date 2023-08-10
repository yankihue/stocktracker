# path/to/your/proj/src/cfehome/celery.py
import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocktracker.settings")

app = Celery("stocktracker")

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# We used CELERY_BROKER_URL in settings.py instead of:
# app.conf.broker_url = ''

# We used CELERY_BEAT_SCHEDULER in settings.py instead of:
# app.conf.beat_scheduler = ''django_celery_beat.schedulers.DatabaseScheduler'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# Below is for illustration purposes. We
# configured so we can adjust scheduling
# in the Django admin to manage all
# Periodic Tasks like below
app.conf.beat_schedule = {
    "populate_stock_price": {
        "task": "stocks.tasks.populate_stock_price",
        "schedule": 13.0,  # Free tier rate limit is 5 requests per minute, this barely gets us over
    },
    "sync_stocks": {
        "task": "stocks.tasks.sync_stocks",
        "schedule": 600,  # Check every 10 minutes for changes to the stock list that we can sync
    },
}
