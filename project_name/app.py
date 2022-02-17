"""
Файл с главным приложением
"""
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from mount import on_startup_mount

app = FastAPI(version="1.2", default_response_class=ORJSONResponse)

# При старте подключить зависимости
on_startup_mount(app)
