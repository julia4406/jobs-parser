from app.scan_dou_ua import get_dou_jobs
from app.celery_app import send_jobs_from_dou


def new_jobs_on_dou():
    jobs = get_dou_jobs()
    if jobs:
        send_jobs_from_dou.delay(jobs)


if __name__ == "__main__":
    print("Script started!")
    new_jobs_on_dou()
