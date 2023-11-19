import os

from celery import Celery

celery_app = None

REDIS_URL = os.environ.get("REDIS_URL", "myredis")
REDIS_PASS = "oQBeaMIF7SX0C71mJH8Pod216QYpNBbA1Qv3B2icMCJdUKKgfuEIwqHSnZi6etLpshgv7NLiuuwDRGjmGmH2RIAdVuvoZl68dTEv03q0A9NwSyo2kcCdGsFE9Xsk8E5K"

celery_app = Celery(
    "worker",
    backend=f"redis://:{REDIS_PASS}@{REDIS_URL}:6379/0",
    broker=f"redis://:{REDIS_PASS}@{REDIS_URL}:6379/1"
)
celery_app.conf.task_routes = {
    "app.app.worker.celery_worker.test_celery": "test-queue"}

celery_app.conf.update(task_track_started=True)
