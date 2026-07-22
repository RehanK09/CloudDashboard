import logging
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "cloud.log")


if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)


class CloudLogger:

    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def warning(message):
        logging.warning(message)

    @staticmethod
    def error(message):
        logging.error(message)

    @staticmethod
    def upload_started(filename, size="Unknown"):

        logging.info(
            f"UPLOAD STARTED | {filename} | {size}"
        )

    @staticmethod
    def upload_finished(filename, size="Unknown"):

        logging.info(
            f"UPLOAD SUCCESS | {filename} | {size}"
        )

    @staticmethod
    def upload_failed(filename):

        logging.error(
            f"UPLOAD FAILED | {filename}"
        )

    @staticmethod
    def mounted():

        logging.info(
            "Drive Mounted"
        )

    @staticmethod
    def unmounted():

        logging.info(
            "Drive Unmounted"
        )

    @staticmethod
    def dashboard_opened():

        logging.info(
            "Dashboard Started"
        )

    @staticmethod
    def dashboard_closed():

        logging.info(
            "Dashboard Closed"
        )


def latest_logs(limit=100):

    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as f:

        lines = f.readlines()

    return lines[-limit:]