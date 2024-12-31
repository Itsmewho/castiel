import os
import logging
from celery import Celery
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()


def make_celery(app_name=__name__):
    broker_url = f"redis://{os.getenv('REDIS_HOST')}:{int(os.getenv('REDIS_PORT'))}/{int(os.getenv('REDIS_BROKER_DB'))}"
    backend_url = f"redis://{os.getenv('REDIS_HOST')}:{int(os.getenv('REDIS_PORT'))}/{int(os.getenv('REDIS_BACKEND_DB'))}"

    return Celery(app_name, broker=broker_url, backend=backend_url, include=["tasks"])


celery = make_celery()


LOG_FOLDER = os.path.join(os.path.dirname(__file__), "log")
os.makedirs(LOG_FOLDER, exist_ok=True)  # Ensure the log folder exists

log_file = os.path.join(LOG_FOLDER, "celery_task.log")
handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger("celery")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

celery.conf.update(
    task_track_started=True, result_expires=3600, task_ignore_result=False
)
