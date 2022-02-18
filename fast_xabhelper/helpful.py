from os import environ
from os import path
from shutil import copytree, rmtree

from loguru import logger


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
