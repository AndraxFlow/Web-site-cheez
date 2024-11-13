import os

from dotenv import load_dotenv

load_dotenv()

__all__ = [
    'SECRET_TOKEN',
    'SESSION_LIFETIME_DAYS',
    'DB_HOST',
    'DB_PORT',
    'DB_USER',
    'DB_PASSWORD',
    'DB_DATABASE',
    'HTTP_HOST',
    'HTTP_PORT',
    'DEBUG',
]

SECRET_TOKEN: str = os.getenv("SECRET_TOKEN")
SESSION_LIFETIME_DAYS: int = int(os.getenv("SESSION_LIFETIME_DAYS"))

DB_HOST: str= os.getenv("DB_HOST")
DB_PORT: int = int(os.getenv("DB_PORT"))
DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")
DB_DATABASE: str = os.getenv("DB_DATABASE")
HTTP_HOST: str = os.getenv("HTTP_HOST")
HTTP_PORT: int = int(os.getenv("HTTP_PORT"))

DEBUG: bool = os.getenv("DEBUG").lower() in ("t", "true", "1")