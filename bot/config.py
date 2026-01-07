import os
import re
import sys
from loguru import logger

BOT_TOKEN = os.environ.get("BOT_TOKEN")
DEBUG = os.environ.get("DEBUG", "False").lower() in ("1", "true", "yes")

MUFFLON_PATTERN = re.compile(r"муф(?:л(?:о(?:н)?)?)?", re.IGNORECASE)

if not BOT_TOKEN:
    logger.error("BOT_TOKEN is not set!")
