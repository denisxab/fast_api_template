"""
Файл для подключения зависимостей к приложению
"""
from abc import abstractmethod
from os import environ

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger


class BaseMount:
    """
    Шаблон для подключения различных вещей к приложению.

    Производите импорты `fast_xabhelper` внутри методов
    """

    def __init__(self, _app: FastAPI):
        self.app = _app

    @abstractmethod
    def mount_model(self):
        """
        Подключаем модели
        """

    def mount_other_dependents(self):
        """
        Подключение зависимостей к приложению
        """
        ...

    @abstractmethod
    def mount_route(self):
        """
        Подключение путей к приложению
        """
        ...

    def mount_static(self):
        """
        Подключить папку со статическими файлами
        """
        self.app.mount(
            # `URL` путь
            "/static",
            # Директория в которой искать статические файлы
            StaticFiles(directory=environ["STATIC_PATH"]),
            # Это имя будем использовать в
            # `{{ url_for('$name$', path='/$Файл$.css') ) }}`
            name="static")

    def mount_src(self):
        """

        :return:
        """

    @abstractmethod
    def mount_admin_panel(self):
        """
        Подключение админ панелей
        """
        ...

    def run_mount(self):
        """
        Запустить монтирование
        """
        self.mount_route()
        logger.info(f'APP-{environ["ALL_APP"]}')
        self.mount_model()
        logger.info(f'MODEL-{environ["ALL_MODEL"]}')
        self.mount_admin_panel()
        self.mount_other_dependents()
        self.mount_static()
