"""
Файл для выполнения инструкций
"""

from asyncio import run
from typing import Type

from fast_xabhelper.mount_logic import BaseMount


class Mange:
    def __init__(self, mount_onj: Type[BaseMount], path_settings: str = "./settings.py"):

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

    def include_mount(self, _app, mount_onj: Type[BaseMount]):
        """
        Подключаем зависимости
        """
        mount_onj.run_mount(_app)

    def include_db(self):
        """
        Подключить БД
        """
        from fast_xabhelper.database import engine, Base
        return engine, Base

    def main(self, _app, command: str):
        """
        Главный метод запуска сценария
        """
        match command:
            case "init_models":
                engine, Base = self.include_db()
                run(self.init_models(engine, Base))

            case "run_dev":
                # @_app.on_event("startup")
                # async def on_startup():
                #     """
                #     Задачи которы нужно выполнить при запуске сервера
                #     """

                self.include_mount(_app, self.mount_onj)

    @staticmethod
    async def init_models(engine, Base):
        """
        Создать таблицы в БД
        """
        async with engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all(engine, tables=Photo))
            await conn.run_sync(Base.metadata.create_all)
