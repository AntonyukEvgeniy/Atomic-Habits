import eventlet
eventlet.monkey_patch(os=True, select=True, socket=True, thread=True, time=True)
# Then import other modules
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# Create celery app
app = Celery("config")
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")
# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
# Configure Celery Beat Schedule


# app.conf.beat_schedule = {
#     "check-inactive-users": {
#         "task": "users.tasks.deactivate_inactive_users",
#         "schedule": timedelta(seconds=30),  # Запускать каждые 30 секунд
#     },
# }
# Timezone settings
app.conf.timezone = "Europe/Moscow"
