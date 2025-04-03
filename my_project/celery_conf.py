from celery import Celery
import os
from datetime import timedelta
from accounts.tasks import send_otp_code


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")

app_celery = Celery("my_project")
app_celery.autodiscover_tasks(["accounts"])
from celery import Celery
from accounts.tasks import send_otp_code

app = Celery("my_project")
app.autodiscover_tasks(["accounts"])




app_celery.conf.broker_url = "amqp://guest:guest@localhost:5672//"
app_celery.conf.result_backend = "rpc://" 
app_celery.conf.task_serializer = "json"
app_celery.conf.result_serializer = "pickle"
app_celery.conf.accept_content = ["json","pickle"]
app_celery.conf.result_expires = timedelta(days=1)
app_celery.conf.task_always_eager = False
app_celery.conf.worker_prefetch_multiplier = 4
