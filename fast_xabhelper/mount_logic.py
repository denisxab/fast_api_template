"""
Файл для подключения зависимостей к приложению
"""
from abc import abstractstaticmethod
from os import environ


class BaseMount:
    """
    Шаблон для подключения различных вещей к приложению
    """

    @abstractstaticmethod
    def mount_model():
        """
        Подключаем модели
        """

    @staticmethod
    def mount_other_dependents(_app):
        """
        Подключение зависимостей к приложению
        """
        ...

    @abstractstaticmethod
    def mount_route(_app):
        """
        Подключение путей к приложению
        """
        ...

    @abstractstaticmethod
    def mount_static(_app):
        """
        Подключение статических файлов
        """
        ...

    @abstractstaticmethod
    def mount_admin_panel():
        """
        Подключение админ панелей
        """
        ...

    @classmethod
    def run_mount(cls, _app):
        cls.mount_route(_app)
        print(environ["ALL_APP"])
        cls.mount_model()
        cls.mount_admin_panel()
        cls.mount_other_dependents(_app)
        cls.mount_static(_app)


def on_startup_mount(app):
    """
    При старте подключить зависимости
    """
