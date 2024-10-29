import os
import logging

log_level = os.getenv("LOG_LEVEL", "INFO").upper()

logger = logging.getLogger("AppLogger")
logger.setLevel(log_level)

console_handler = logging.StreamHandler()
console_handler.setLevel(log_level)

formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
