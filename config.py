import os
from pathlib import Path

from fastapi.security import HTTPBearer
from pyhocon import ConfigFactory

FASTAPI_ENV = os.getenv("FASTAPI_ENV", "local")

BASE_DIR = Path(__file__).resolve().parent

CONF_ENV = {"testing": "testing.conf", "local": "local.conf"}
config = ConfigFactory.parse_file(BASE_DIR / CONF_ENV[FASTAPI_ENV])

DATABASE_URL = config.get("database_url")

CORS_ORIGINS = config.get("cors.origins", [])

SECRET_KEY = config.get("secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

HTTP_BEARER = HTTPBearer()
