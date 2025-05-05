import html
import os

import requests
from dotenv import load_dotenv

from app.logging_settings import logger


load_dotenv()

BASE_TG_URL = "https://api.telegram.org"
API_URL = f"{BASE_TG_URL}/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage"


def message_to_telegram(msg: dict):
    description = html.escape(msg["description"])[:2000]

    text = (
        f"<b>{msg['title']} ({msg['experience']})</b>\n"
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


def message_login_djinni_failed(error: str):
    payload = {
        "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
        "text": f"<b>❌ Login to Djinni failed:</b>\n<pre>{error}</pre>",
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    try:
        requests.post(API_URL, data=payload)
    except Exception as ex:
        print("Failed to send Telegram message:", ex)
