import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("trading_platform")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "refresh-quotes": {"task": "market.tasks.refresh_quotes", "schedule": 10.0},
    "process-pending-orders": {"task": "trading.tasks.process_pending_orders", "schedule": 5.0},
    "run-bots": {"task": "bot.tasks.run_all_bots", "schedule": 60.0},
}