"""Application configuration, read from environment variables / .env."""
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    IPAPI_BASE_URL = os.getenv("IPAPI_BASE_URL", "https://ipapi.co")
    IPAPI_KEY = os.getenv("IPAPI_KEY", "")
    IPIFY_V4_URL = "https://api.ipify.org"
    IPIFY_V6_URL = "https://api6.ipify.org"
    HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "5"))
    CACHE_TTL = int(os.getenv("CACHE_TTL", "86400"))
    DB_PATH = os.getenv("DB_PATH", "instance/ipatlas.db")
