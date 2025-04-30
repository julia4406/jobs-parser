import os
from dotenv import load_dotenv
from celery import Celery

from app import cache_checker
from app.bot import message_to_telegram
from app.logging_settings import logger

load_dotenv()

celery_app = Celery(
    "jobs_parser",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/1"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/2"),
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Kyiv",
    enable_utc=True,
)


@celery_app.task
def send_jobs_from_dou(jobs: list):
    for job in jobs:
        try:
            if not cache_checker.is_sent(job["url"]):
                message_to_telegram(job)
                print("Well done!")
                cache_checker.mark_as_sent(job["url"])
        except Exception as e:
            logger.error(f"Error sending job {job['url']}: {e}")
