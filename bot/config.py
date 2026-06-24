import os
import re
from pathlib import Path

from loguru import logger
from dataclasses import dataclass

from environs import Env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

BOT_TOKEN = env("BOT_TOKEN")
DEBUG = env("DEBUG", "False").lower() in ("1", "true", "yes")

if not BOT_TOKEN:
    logger.error("BOT_TOKEN is not set!")

MUFFLON_PATTERN = re.compile(r"муф(?:л(?:о(?:н)?)?)?", re.IGNORECASE)

# DATABASE
POSTGRESQL_HOST = env("POSTGRES_HOST", "postgres")
POSTGRESQL_PORT = env("POSTGRES_PORT", "5432")
POSTGRESQL_DB = env("POSTGRES_DB", "muflon_bot_db")
POSTGRESQL_USERNAME = env("POSTGRES_USER", "postgres")
POSTGRESQL_PASSWORD = env("POSTGRES_PASSWORD", "postgres")

SQLALCHEMY_DATABASE_URI = "postgresql+asyncpg://{username}:{password}@{host}:{port}/{dbname}".format(
    username=POSTGRESQL_USERNAME,
    password=POSTGRESQL_PASSWORD,
    host=POSTGRESQL_HOST,
    port=POSTGRESQL_PORT,
    dbname=POSTGRESQL_DB,
)

# REDIS
REDIS_HOST = env("REDIS_HOST", "redis")
REDIS_PORT = env("REDIS_PORT", "6379")
REDIS_PASSWORD = env("REDIS_PASSWORD", "redis")


ROOT_DIR: Path = Path(__file__).parent.resolve()


@dataclass
class StaticPaths:
    cool_muflon_path = ROOT_DIR / "static" / "images" / "muflon_cool.png"

