import os

from celery import Celery

celery = Celery(
    "jobs_checker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1"),
)

celery.conf.timezone = "UTC"
celery.conf.beat_scheduler = "celery.beat.RedisScheduler"
celery.conf.beat_schedule = {
    "check_job_every_hour": {
        "task": "app.tasks.check_new_jobs",
        "schedule": 3600.0,
    },
}
