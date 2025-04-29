import html
import json
import os
import requests
from dotenv import load_dotenv

from app.logging_settings import logger


load_dotenv()
API_URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage"

def message_to_telegram(msg: dict):
    description = html.escape(msg["description"])[:2000]

    text = (
        f"<b>{msg['title']}</b>\n"
        f"{msg['date']}\n"
        f"<b>{msg['company']}</b>\n"
        f"{description}\n"
        f"<a href='{msg['url']}'>Пуньк</a>"
    )

    payload = {
        "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }

    response = requests.post(API_URL, data=payload)

    if response.status_code != 200:
        logger.error(f"Error: {response.status_code} - {response.text}")
    else:
        logger.info("Vacancy sent.")


def send_all_jobs():
    with open("jobs.json", "r", encoding="utf-8") as f:
        jobs = json.load(f)

    for job in jobs:
        message_to_telegram(job)


if __name__ == "__main__":
    send_all_jobs()
