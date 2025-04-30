import logging
import os
from logging.handlers import RotatingFileHandler


log_directory = "/bot/logs"
os.makedirs(log_directory, exist_ok=True)

log_path = os.path.join(log_directory, "jobs_telegram.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)

file_handler = RotatingFileHandler(
    log_path,
    maxBytes=4_000,
    backupCount=1
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
