"""
Файл для подключения зависимостей к приложению
"""
__all__ = ["BaseMount"]

import os.path
from abc import abstractmethod
from os import environ
from typing import Union, Type
from logsmal import logger
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

try:
    from sqlalchemy.orm import DeclarativeMeta
except ImportError:
    logger.info(
        f"{__file__} Ошибка импорта: from sqlalchemy.orm import DeclarativeMeta")

from mg_sql.sql_async.model_logic import RawSqlModel

class BaseAdd:
    """
    Сборник функций для монтирования утилит к проекту
    """

    def __init__(self, _app: FastAPI):
        self.app = _app

    def add_app(
            self,
            name: str,
            route: APIRouter,
            model: list[Union[Type[DeclarativeMeta],
                              Type[RawSqlModel]]] = None,
            app: Union[FastAPI, APIRouter] = None,
    ):
        """
        :param name:  Имя для приложения
        :param route: Готовый APIRouter
        :param model: SQL модель на основе `DeclarativeMeta` или `RawSqlModel`
        :param static: Путь к стоическим файлам у приложения
        :param app: Главное приложение, или другой уже ранее изданный путь
        :return:
        """
        # Если не указано приложение, то берем основное
        if app is None:
            app = self.app
        if route:
            # Добавляем URL пути
            self._add_route(route=route, app=app)
        if model:
            for _m in model:
                # Добавляем модели
                self._add_model(model=_m)
                environ["ALL_MODEL"] += f':{_m}'
        environ["ALL_APP"] += f":{name}"

    @staticmethod
    def _add_route(
            route: APIRouter,
            app: Union[FastAPI, APIRouter],
    ):
        """
        Добавить путь в приложение или в другой путь.

        @param app: Главное приложение или любой путь. По умолчанию используется
        основное приложение, но так же можно передавать `route` и делать вложенные пути
        @param route: Путь
        """
        # Добавить путь в приложение
        app.include_router(route)

    @staticmethod
    def _add_model(model: Union[Type[DeclarativeMeta], Type[RawSqlModel]]):
        """
        Добавить модель в отслеживание
        """
        environ["ALL_MODEL"] += f":{model.__name__}"
        # Если создание через наследование RawSqlModel, то добавляем объект в словарь `_all_tables` который
        # используется в функции `init_models`
        if issubclass(model, RawSqlModel):
            model: RawSqlModel
            RawSqlModel.all_tables[model.table_name] = model


class BaseMount(BaseAdd):
    """
    Шаблон для подключения различных вещей к приложению.

    Производите импорты `vetcin_pack_fastapi` внутри методов
    """

    def run_mount(self):
        """
        Запустить монтирование
        """
        self.mount_app()
        logger.info(f'{environ["ALL_APP"]}', flags=["APP"])
        logger.info(f'{environ["ALL_MODEL"]}', flags=["MODEL"])
        self._mount_root_static()

    @abstractmethod
    def mount_app(self):
        """
        Общая форма для подключения приложений, для подключения приложения используйте метод `add_app`
        """
        ...

    def _mount_root_static(self):
        """
        Подключить папку со статическими файлами
        """

        if environ["STATIC_PATH"]:
            if os.path.exists(environ["STATIC_PATH"]):
                self.app.mount(
                    # `URL` путь
                    "/static",
                    # Директория в которой искать статические файлы
                    StaticFiles(directory=environ["STATIC_PATH"]),
                    # Это имя будем использовать в
                    # `{{ url_for('$name$', path='/$Файл$.css') ) }}`
                    name="static"
                )
            else:
                logger.error(
                    f"Нет обязательный папки static по пути: {environ['STATIC_PATH']}", "_mount_root_static")
                exit(0)
