import os

from celery import Celery

celery = Celery(
    "jobs_checker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6381/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6381/1"),
)

celery.conf.timezone = "UTC"
celery.conf.beat_schedule = {
    "check_job_every_hour": {
        "task": "app.tasks.check_new_jobs",
        "schedule": 3600.0,
    },
}
