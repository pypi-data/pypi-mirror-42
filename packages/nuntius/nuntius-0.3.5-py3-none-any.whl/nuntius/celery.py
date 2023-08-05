from __future__ import absolute_import, unicode_literals
from celery import Celery

nuntius_celery_app = Celery("nuntius")

nuntius_celery_app.conf.task_default_routing_key = "nuntius"
nuntius_celery_app.conf.task_started = True

nuntius_celery_app.config_from_object(
    "django.conf:settings", namespace="NUNTIUS_CELERY"
)
