from os import environ
from pathlib import Path

from fastapi.templating import Jinja2Templates

user: str = environ["ADMIN_USER_NAME"]
password: str = environ["ADMIN_PASSWORD"]


def get_tamplate():
    # Указываем директорию, где искать шаблоны
    return Jinja2Templates(directory=Path(__file__).resolve().parent / "templates")
