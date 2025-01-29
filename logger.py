import logging
import os
from datetime import datetime

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
log_filepath = os.path.join(LOG_DIR, log_filename)

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler()
    ]
)

def log_info(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)

def log_error(message):
    logging.error(message)

def log_debug(message):
    logging.debug(message)
