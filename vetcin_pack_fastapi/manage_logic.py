"""
Файл для выполнения управляющих команд
"""
import asyncio
from enum import Enum
from os import environ

import uvicorn

from .manage_base import BaseManage


class allow_command(Enum):
    """
    Доступные команды
    """
    #: Инициализация проекта
    init_app = "init"
    #: Создать все таблицы на основе моделей
    init_models = "init_models"
    #: Удалить все таблицы
    delete_models = "delete_models"
    #: Запустить `ASGI` сервер `uvicorn`
    run_dev = "run_dev"
    #: Создать шаблонное приложение
    create_app = "create_app"


class Mange(BaseManage):
    """
    Класс для выполнения инструкций
    """

    def run_command(self, command: allow_command, *args, **kwargs):
        """
        Главный метод запуска сценария
        """
        match command.name:
            case command.run_dev.name:
                """
                if __name__ == "__main__":
                    mg.main("run_dev")
                """
                uvicorn.run(
                    "main:app",
                    host=environ["HOST_WEB"],
                    port=int(environ["PORT_WEB"]),
                    reload=environ["RELOAD_WEB"]
                )

            case command.init_models.name:
                asyncio.run(self.init_models())

            case command.delete_models.name:
                asyncio.run(self.delete_models())

            case command.init_app.name:
                pass

            case command.create_app.name:
                self.create_app(name_app=kwargs['name_app'])
