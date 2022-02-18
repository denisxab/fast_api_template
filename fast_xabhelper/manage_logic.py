"""
Файл для выполнения инструкций
"""
import os
from asyncio import run
from enum import Enum
from typing import Type

import uvicorn
from fastapi import FastAPI
from loguru import logger

from mount_logic import BaseMount


class comd(Enum):
    """Доступные команды"""
    # Инициализация проекта
    init_app = "init"
    # Создать все таблицы на основе моделей
    init_models = "init_models"
    # Удалить все таблицы
    delete_models = "delete_models"
    # Запустить `ASGI` сервер `uvicorn`
    run_dev = "run_dev"


class Mange:
    """
    Класс для выполнения инструкций
    """

    def __init__(self, mount_onj: Type[BaseMount], _app: FastAPI, path_settings: str = "./settings.py"):
        self.app = _app
        self.mount_onj = mount_onj
        self.mount_onj = mount_onj
        # Подключить Настройки
        self.include_settings(path_settings)

    @staticmethod
    def include_settings(path_settings: str):
        """
        Подключить настройки проекта
        """
        # Подключаем переменные окружения из настроек проекта
        from fast_xabhelper.settings_logic import mount_env
        mount_env(path_settings)

    def include_mount(self):
        """
        Подключаем зависимости приложения
        """
        self.mount_onj(self.app).run_mount()

    @staticmethod
    def include_db():
        """
        Подключить БД
        """
        from fast_xabhelper.database_pack.database import engine, Base
        return engine, Base

    def run_command(self, command: comd):
        """
        Главный метод запуска сценария
        """
        match command.name:
            case command.init_models.name:
                self.include_mount()
                engine, Base = self.include_db()
                run(self.init_models(engine, Base))

            case command.delete_models.name:
                self.include_mount()
                engine, Base = self.include_db()
                run(self.delete_models(engine, Base))

            case command.init_app.name:
                """
                Не запускайте эту команду в if __name__ == "__main__" !
                """

                @self.app.on_event("startup")
                async def on_startup():
                    """
                    Задачи которы нужно выполнить при запуске сервера
                    """
                    logger.success(
                        f"Сервер запущен\nhost={os.environ['HOST_WEB']}, port={os.environ['PORT_WEB']}, reload={os.environ['RELOAD_WEB']}")
                    self.include_mount()

                @self.app.on_event("shutdown")
                async def on_shutdown():
                    """
                    Задачи которы нужно выполнить при запуске сервера
                    """
                    from fast_xabhelper.session_pack.session_base import exit_
                    exit_()

            case command.run_dev.name:
                """
                if __name__ == "__main__":
                    mg.main("run_dev")
                """

                uvicorn.run("main:app",
                            host=os.environ["HOST_WEB"],
                            port=int(os.environ["PORT_WEB"]),
                            reload=os.environ["RELOAD_WEB"])

    @staticmethod
    async def init_models(engine, Base):
        """
        Создать таблицы в БД
        """
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info(f"Таблицы созданы {list(Base.metadata.tables.keys())}")

    @staticmethod
    async def delete_models(engine, Base):
        """
        Создать таблицы в БД
        """
        if input("Вы действительно хотите удалить все таблицы ?") == "YES":
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all())
            logger.warning(f"Таблицы удалены {list(Base.metadata.tables.keys())}")

        else:
            logger.warning("Таблицы не удалены")
