# import os.path
from os import path, environ
from shutil import copytree, rmtree
from typing import Union

from fastapi import FastAPI, APIRouter
from loguru import logger

STATIC_PATH = path.join(environ["BASE_DIR"], "static")


def copy_static(path_static: str, name_app: str):
    if environ["COPY_STATIC"] == "True":
        # Копировать статические файлы
        # Откуда копировать
        in_path = path_static
        # Куда копировать
        out_path = path.join(STATIC_PATH, name_app)

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
