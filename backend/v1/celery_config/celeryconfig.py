import os

imports = ("tasks",)
task_serializer = 'json'
result_accept_content = ['json']
result_serializer = 'json'
accept_content = ['json']
broker_url = os.environ.get('CELERY_BROKER_URL')
timezone = 'America/Bogota'
broker_pool_limit = 1 # Will decrease connection usage
broker_heartbeat = None # We're using TCP keep-alive instead
broker_connection_timeout = 30 # May require a long timeout due to Linux DNS timeouts etc
result_backend = 'rpc://' # AMQP is not recommended as result backend as it creates thousands of queues
result_persistent = False
event_queue_expires = 60 # Will delete all celeryev. queues without consumers after 1 minute.
worker_prefetch_multiplier = 1 # Disable prefetching, it's causes problems and doesn't help performance
worker_concurrency = 2 # If you tasks are CPU bound, then limit to the number of cores, otherwise increase substainally
worker_max_tasks_per_child = 1
task_ignore_result = True