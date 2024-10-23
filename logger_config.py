import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = "get_stores_and_devices.log"
MAX_LOG_SIZE = 3 * 1024 * 1024  # 3 MB
BACKUP_COUNT = 3

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, LOG_FILE),
            "maxBytes": MAX_LOG_SIZE,
            "backupCount": BACKUP_COUNT,
            "formatter": "default",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": True,
        }
    },
}

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)