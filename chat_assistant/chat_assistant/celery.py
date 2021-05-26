from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_assistant.settings')

app = Celery('chat_assistant')

class Config:
    BROKER_URL = 'redis://redis:6379'
    CELERY_RESULT_BACKEND = 'redis://redis:6379'

app.config_from_object(Config)
app.conf.update(worker_max_memory_per_child=300000)  # 300MB
app.autodiscover_tasks()
