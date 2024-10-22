import os

LOG_DIR = "logs"
LOG_FILE = "get_stores_and_devices.log"

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
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, LOG_FILE),
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