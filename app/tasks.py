from celery_app import celery

from app import cache_checker
from app.bot import message_to_telegram
from app.scan_dou_ua import get_dou_jobs


@celery.task
def check_new_jobs():
    jobs = get_dou_jobs()
    for job in jobs:
        if not cache_checker.is_sent(job["url"]):
            message_to_telegram(job)
            cache_checker.mark_as_sent(job["url"])
