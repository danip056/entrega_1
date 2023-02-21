from __future__ import absolute_import, unicode_literals
from celery import Celery


dsc_app = Celery('dsc_app')
dsc_app.config_from_object('celery_config.celeryconfig')


@dsc_app.task
def print_sum():
    print("sum is: ", 2+2)

dsc_app.autodiscover_tasks()