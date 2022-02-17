"""
Файл с главным приложением
"""
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from mount import mount_dependents

app = FastAPI(version="1.2", default_response_class=ORJSONResponse)


@app.on_event("startup")
async def on_startup():
    """
    Задачи которы нужно выполнить при запуске сервера
    """
    # Примонтировать зависимости
    mount_dependents()
