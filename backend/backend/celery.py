# backend/celery.py
import os
from celery import Celery

# Set default Django settings module for 'celery' command-line program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Load settings from Django's settings.py using the 'CELERY_' namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all registered Django apps
app.autodiscover_tasks()