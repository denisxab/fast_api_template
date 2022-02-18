"""
Файл для подключения зависимостей к приложению
"""
import os
import threading
from abc import abstractmethod
from os import environ, path, system
from typing import Type, Union

from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from loguru import logger
from mg_file.file.base_file import concat_absolute_dir_path
from sqlalchemy.orm import DeclarativeMeta

from fast_xabhelper.helpful import copy_static


class BaseMount:
    """
    Шаблон для подключения различных вещей к приложению.

    Производите импорты `fast_xabhelper` внутри методов
    """

    @abstractmethod
    def mount_model(self):
        """
        Подключаем модели
        """

    @abstractmethod
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

    @abstractmethod
    def mount_admin_panel(self):
        """
        Подключение админ панелей
        """
        ...

    @abstractmethod
    def mount_src_svelte(self):
        """
        Добавить папку со скриптами `Svelte`
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

    """
    Не обязательно переопределять
    """

    def __init__(self, _app: FastAPI):
        self.app = _app

    def run_mount(self):
        """
        Запустить монтирование
        """
        self.mount_src_svelte()
        self.mount_route()
        logger.info(f'APP-{environ["ALL_APP"]}')
        self.mount_model()
        logger.info(f'MODEL-{environ["ALL_MODEL"]}')
        self.mount_admin_panel()
        self.mount_other_dependents()
        self.mount_static()

    @staticmethod
    def add_src_svelte(PathApp: str,
                       NameApp: str,
                       PathOutStatic: str = None,
                       PathSrc: str = None,
                       PathByUrl: str = None,
                       PathOutTemplate: str = None,
                       AutoComplete: bool = False
                       ):
        """
        Добавим в очередь на выполнение команды компиляции скриптов на `Svelte`.

        @param PathOutStatic: Путь для скомпилированных файлов
        @param NameApp: Имя приложения
        @param PathSrc: Путь до папки с скриптами `Svelte`
        @param PathByUrl: Какой  URL будет в `HTML` файле. Нужен для маршрутизации
        @param PathApp: Путь к приложению
        @param PathOutTemplate:  Путь для сохранения готового html файла
        @param AutoComplete: Следить за изменениями в коде и перекомпилировать скрипты
        @return:
        """

        def self__():

            cmd = "npm --prefix {0} run build -- {1}{2}{3}{4}{5}{6}".format(
                concat_absolute_dir_path(__file__, "svelte_pack"),
                f" --env PathOutStatic={PathOutStatic}" if PathOutStatic else "",
                f" --env PathSrc={PathSrc}" if PathSrc else "",
                f" --env PathByUrl={PathByUrl}" if PathByUrl else f" --env PathByUrl=/static/{NameApp}",
                f" --env PathApp={PathApp}" if PathApp else "",
                f" --env AutoComplete=true" if AutoComplete else " --env AutoComplete=false",
                f" --env PathOutTemplate={PathOutTemplate}" if PathOutTemplate else "",
                # Путь к главной папке с приложением где находятся статические файлы
                f" --env MainStaticPath={os.path.join(os.environ['STATIC_PATH'], NameApp)}",
            )
            logger.info(cmd)
            system(cmd)

        if AutoComplete:
            """
            Так как мы используем автоперекампеляцию кода при изменении файлов,
            то для того чтобы поток выполнения не блокировался, мы выполняем команду в отдельном потоке.
            """
            logger.info(f"Создан новый поток: {NameApp}")
            th = threading.Thread(target=self__, args=(), name=f"{NameApp}", daemon=True)
            th.start()
        else:
            self__()

    @staticmethod
    def add_admin_panel(admin_panel):
        """
        Добавить панель в список

        @param admin_panel: AdminPanel:
        """
        from fast_xabhelper.admin_pack.admin_base import Admin
        Admin.arr_admin[admin_panel.name] = admin_panel

    @staticmethod
    def add_model(model: Type[DeclarativeMeta]):
        """
        Добавить модель
        """
        environ["ALL_MODEL"] += f":{model.__name__}"

    @staticmethod
    def add_route(_app: Union[FastAPI, APIRouter],
                  route: APIRouter, *,
                  name: str,
                  path_static: str = "",
                  absolute: bool = False):
        """
        Добавить путь в приложение или в другой путь. При этом если COPY_STATIC="True"`
        будет происходить копирование статических файлов из пути `path_static`

        @param _app: Главное приложение или любой путь
        @param route: Путь
        @param name: Имя папки в котором расположен путь
        @param path_static: Путь к статическим файлам, они будут копированные если
        переменная окружения `COPY_STATIC="True"`
        @param absolute: Вы можете указать что `path_static` имеет абсолютный путь
        """
        # Добавить приложение в список
        environ["ALL_APP"] += f":{name}"
        # Добавить путь в приложение
        _app.include_router(route)
        # Копируем статические файлы
        if path_static:
            copy_static(
                # Если указан абсолютный путь, то взять его.
                path_static if absolute else path.join(environ["BASE_DIR"], path_static),
                name)
