from app.logging_settings import logger
from app.celery_app import celery_app
from app import cache_checker
from app.bot import message_to_telegram


@celery_app.task
def send_jobs_from_dou(jobs: list):
    for job in jobs:
        try:
            if not cache_checker.is_parsed(job["url"]):
                message_to_telegram(job)
                print("Done again!")
                cache_checker.mark_as_parsed(job["url"])
        except Exception as e:
            logger.error(f"Error sending job {job['url']}: {e}")
