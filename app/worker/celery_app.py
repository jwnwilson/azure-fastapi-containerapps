import os

from celery import Celery

celery_app = None

REDIS_URL = os.environ.get("REDIS_URL", "redis.internal.purplebush-f96f867f.northeurope.azurecontainerapps.io")

celery_app = Celery(
    "worker",
    backend=f"redis://:password123@{REDIS_URL}:6379/0",
    broker=f"redis://:password123@{REDIS_URL}:6379/1"
)
celery_app.conf.task_routes = {
    "app.app.worker.celery_worker.test_celery": "test-queue"}

celery_app.conf.update(task_track_started=True)
