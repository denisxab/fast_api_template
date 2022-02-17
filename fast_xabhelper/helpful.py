from os import environ
from os import path
from shutil import copytree, rmtree
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
