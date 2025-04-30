from app import cache_checker
from app.bot import message_to_telegram
from app.logging_settings import logger
from app.scan_dou_ua import get_dou_jobs
from app.tasks import send_jobs_from_dou


def new_jobs_on_dou():
    jobs = get_dou_jobs()
    if jobs:
        # send_jobs_from_dou.delay(jobs)
        for job in jobs:
            try:
                if not cache_checker.is_sent(job["url"]):
                    message_to_telegram(job)
                    print("Done!")
                    cache_checker.mark_as_sent(job["url"])
            except Exception as e:
                logger.error(f"Error sending job {job['url']}: {e}")


if __name__ == "__main__":
    print("Script started!")
    new_jobs_on_dou()
