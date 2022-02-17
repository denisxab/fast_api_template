"""
Файл для выполнения инструкций
"""

from asyncio import run
from typing import Type

import uvicorn
from fastapi import FastAPI

from fast_xabhelper.mount_logic import BaseMount


class Mange:
    def __init__(self, mount_onj: Type[BaseMount], _app: FastAPI, path_settings: str = "./settings.py"):
        self.app = _app
        self.mount_onj = mount_onj
        self.mount_onj = mount_onj
        # Подключить Настройки
        self.include_settings(path_settings)

    def include_settings(self, path_settings: str):
        """
        Подключить настройки проекта
        """
        # Подключаем переменные окружения из настроек проекта
        from fast_xabhelper.settings_logic import mount_env
        mount_env(path_settings)

    def include_mount(self):
        """
        Подключаем зависимости
        """
        self.mount_onj(self.app).run_mount()

    def include_db(self):
        """
        Подключить БД
        """
        from fast_xabhelper.database import engine, Base
        return engine, Base

    def main(self, command: str):
        """
        Главный метод запуска сценария
        """
        match command:
            case "init_models":
                engine, Base = self.include_db()
                run(self.init_models(engine, Base))
            case "init":
                """
                Не запускайте эту команду в if __name__ == "__main__" !
                """

                @self.app.on_event("startup")
                async def on_startup():
                    """
                    Задачи которы нужно выполнить при запуске сервера
                    """
                    self.include_mount()

            case "run_dev":
                """
                if __name__ == "__main__":
                    mg.main("run_dev")
                """
                uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    @staticmethod
    async def init_models(engine, Base):
        """
        Создать таблицы в БД
        """
        async with engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all(engine, tables=Photo))
            await conn.run_sync(Base.metadata.create_all)


def main(_app, mtt):
    mtt.mount_route(_app)
