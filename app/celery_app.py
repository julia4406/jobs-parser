import os

from celery.schedules import crontab
from dotenv import load_dotenv
from celery import Celery

from app.bot import message_to_telegram
from app.logging_settings import logger
from app.scan_djinni import get_djinni_jobs
from app.scan_dou_ua import get_dou_jobs
from app.urls import LINKS_DOU, LINKS_DJINNI


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

celery_app.conf.beat_schedule = {
    "send_jobs_from_dou_schedule": {
        "task": "app.celery_app.send_jobs_from_dou",
        "schedule": crontab(minute=45, hour="9,13,14,20")
    },
    "send_jobs_from_djinni_schedule": {
        "task": "app.celery_app.send_jobs_from_djinni",
        "schedule": crontab(minute=50, hour="9,13,14,20")
    }
}


@celery_app.task
def send_jobs_from_dou():
    jobs = get_dou_jobs(LINKS_DOU)
    for job in jobs:
        try:
            message_to_telegram(job)
            logger.info("New jobs sent.")

        except Exception as e:
            logger.error(f"Error sending job {job['url']}: {e}")


@celery_app.task
def send_jobs_from_djinni():
    jobs = get_djinni_jobs(LINKS_DJINNI)
    for job in jobs:
        try:
            message_to_telegram(job)
            logger.info("New jobs sent.")

        except Exception as e:
            logger.error(f"Error sending job {job['url']}: {e}")
