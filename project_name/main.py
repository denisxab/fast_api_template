"""
Файл запуска проекта
"""
from uvicorn import run

from settings import mount_env

# Подключаем переменные окружения из настроек
mount_env()

if __name__ == "__main__":
    run("app:app", host="0.0.0.0", port=8000, reload=True)
