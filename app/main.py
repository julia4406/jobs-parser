from app.scan_dou_ua import get_dou_jobs
from app.celery_app import send_jobs_from_dou


def new_jobs_on_dou():
    send_jobs_from_dou.delay()


if __name__ == "__main__":
    print("Poihaly!")
    # new_jobs_on_dou()
