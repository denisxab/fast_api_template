from importlib.machinery import ModuleSpec
from importlib.util import spec_from_file_location, module_from_spec
from os import environ
from os import path
from pathlib import Path
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
    """
    Добавить путь в приложение или в другой путь. При этом если COPY_STATIC="True"`
    будет происходить копирование статических файлов из пути `path_static`

    @param app: Главное приложение или любой путь
    @param route: Путь
    @param name: Имя папки в котором расположен путь
    @param path_static: Путь к статическим файлам, они будут копированные если
    переменная окружения `COPY_STATIC="True"`
    @param absolute: Вы можете указать что `path_static` имеет абсолютный путь
    """
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
    environ["ALL_MODEL"] += f":{model.__name__}"


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


def concat_absolute_dir_path(_file: str, _path: str) -> str:
    """
    Получить абсолютный путь папки и объединить с другим путем

    :param _file:
    :param _path:
    :return:
    """
    return str(Path(_file).resolve().parent / _path)


def absolute_path_dir(_file: str, back: int = 1) -> Path:
    """
    Получить абсолютный путь к своей директории

    :param _file:
    """
    res = Path(_file).resolve()
    for _ in range(back):
        res = res.parent
    return res
