import sys
import os
sys.path.append(
    os.path.dirname(__file__)
)
from celery import shared_task
from handle_task import process_task as _process_task


@shared_task(autoretry_for=(Exception,), max_retries=3 ,default_retry_delay=240, ignore_result=True)
def process_task(id_task):
    _process_task(id_task)
    return True