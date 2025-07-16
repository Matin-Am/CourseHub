from celery import Celery
import os



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")

app_celery = Celery("my_project")




app_celery.conf.broker_url = "amqp://matin:matin@localhost:5672/matin_vhost"
app_celery.conf.task_serializer = "json"
app_celery.conf.accept_content = ["json",]
app_celery.conf.worker_prefetch_multiplier = 1
app_celery.conf.task_ignore_result = True
app_celery.conf.task_acks_late = True

app_celery.autodiscover_tasks()