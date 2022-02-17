"""
Файл запуска проекта
"""
import uvicorn


from settings import mount_env

# Подключаем переменные окружения из настроек
mount_env()

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
