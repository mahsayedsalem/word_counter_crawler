import os
from celery import Celery

CELERY_BROKER_URL = os.getenv("REDISSERVER", "redis://redis_server:6379")
CELERY_RESULT_BACKEND = os.getenv("REDISSERVER", "redis://redis_server:6379")

celery_server = Celery("celery", backend=CELERY_BROKER_URL, broker=CELERY_RESULT_BACKEND)
