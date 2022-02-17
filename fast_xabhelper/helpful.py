import os.path
from shutil import copytree, rmtree

from fastapi import FastAPI, APIRouter
from loguru import logger

# from settings import BASE_DIR, COPY_STATIC

STATIC_PATH = os.path.join(os.environ["BASE_DIR"], "static")


def copy_static(path_static: str, name_app: str):
    if os.environ["COPY_STATIC"] == "True":
        # Копировать статические файлы
        # Откуда копировать
        in_path = path_static
        # Куда копировать
        out_path = os.path.join(STATIC_PATH, name_app)

        if os.path.exists(out_path):
            rmtree(out_path)
            copytree(in_path, out_path)
        else:
            copytree(in_path, out_path)

        logger.info(f"Копирование статических файлов: {out_path}")


def add_route(app: FastAPI, route: APIRouter, name, path_static: str = "", absolute: bool = False):
    # Добавить путь в приложение
    app.include_router(route)
    # Копируем статические файлы
    if path_static:
        copy_static(
            # Если указан абсолютный путь, то взять его.
            path_static if absolute else os.path.join(os.environ["BASE_DIR"], path_static),
            name)
