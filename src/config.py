import os
from datetime import timedelta

from dotenv import load_dotenv
from fastapi_jwt import (
    JwtAccessBearerCookie,
    JwtRefreshBearerCookie,
)
from fastapi.templating import Jinja2Templates

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET") or "FITNESS_SECRET_TOKEN"
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET") or "FITNESS_REFRESH_TOKEN"
ACCESS_TOKEN_EXPIRATION = int(os.getenv("ACCESS_TOKEN_EXPIRATION")) or 1
REFRESH_TOKEN_EXPIRATION = int(os.getenv("REFRESH_TOKEN_EXPIRATION")) or 1

access_security = JwtAccessBearerCookie(
    secret_key=ACCESS_TOKEN_SECRET,
    auto_error=True,
    access_expires_delta=timedelta(hours=ACCESS_TOKEN_EXPIRATION),
)

refresh_security = JwtRefreshBearerCookie(
    secret_key=REFRESH_TOKEN_SECRET, 
    auto_error=True
)

templates = Jinja2Templates(directory="templates")
