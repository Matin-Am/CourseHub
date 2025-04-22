from celery import Celery
import os
from datetime import timedelta


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")

app_celery = Celery("my_project")
app_celery.autodiscover_tasks(["accounts"])



app_celery.conf.broker_url = "amqp://"
app_celery.conf.result_backend = "rpc://" 
app_celery.conf.task_serializer = "json"
app_celery.conf.result_serializer = "pickle"
app_celery.conf.accept_content = ["json","pickle"]
app_celery.conf.result_expires = timedelta(days=1)
app_celery.conf.task_always_eager = False
app_celery.conf.worker_prefetch_multiplier = 4
app_celery.conf.broker_connection_retry_on_startup = True
