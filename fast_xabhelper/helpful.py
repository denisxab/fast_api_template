from importlib.machinery import ModuleSpec
from importlib.util import spec_from_file_location, module_from_spec
from os import environ
from os import path
from shutil import copytree, rmtree
from types import ModuleType
from typing import Optional
from typing import Union, Type

from fastapi import FastAPI, APIRouter
from loguru import logger
from sqlalchemy.orm.decl_api import DeclarativeMeta


def copy_static(path_static: str, name_app: str):
    if environ["COPY_STATIC"] == "True":
        # Копировать статические файлы
        # Откуда копировать
        in_path = path_static
        # Куда копировать
        out_path = path.join(path.join(environ["BASE_DIR"], "static"), name_app)

        if path.exists(out_path):
            rmtree(out_path)
            copytree(in_path, out_path)
        else:
            copytree(in_path, out_path)
        logger.info(f"Копирование статических файлов: {out_path}")


def add_route(app: Union[FastAPI, APIRouter],
              route: APIRouter, *,
              name: str,
              path_static: str = "",
              absolute: bool = False):
    # Добавить приложение в список
    environ["ALL_APP"] += f":{name}"
    # Добавить путь в приложение
    app.include_router(route)
    # Копируем статические файлы
    if path_static:
        copy_static(
            # Если указан абсолютный путь, то взять его.
            path_static if absolute else path.join(environ["BASE_DIR"], path_static),
            name)


def add_model(model: Type[DeclarativeMeta]):
    ...


def read_file_by_module(infile: str) -> ModuleType:
    """
    Импортировать файл как модуль `python`

    @param infile: Путь к `python` файлу
    @return: Модуль `python`
    """
    # указать модуль, который должен быть импортируется относительно пути модуль
    spec: Optional[ModuleSpec] = spec_from_file_location("my_module", infile)
    # создает новый модуль на основе спецификации
    __module: ModuleType = module_from_spec(spec)
    # выполняет модуль в своем собственном пространстве имен,
    # когда модуль импортируется или перезагружается.
    spec.loader.exec_module(__module)
    return __module
