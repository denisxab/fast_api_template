import importlib.util
import os
from importlib.machinery import ModuleSpec
from os.path import splitext
from pathlib import Path
from types import ModuleType
from typing import Optional


def create_file(_path: str, text: str = ''):
    # Функция для создания файлов с текстом
    if not os.path.exists(_path):
        with open(_path, 'w') as _f:
            _f.write(text)


def absolute_path_dir(_file: str, back: int = 1) -> Path:
    """
    Получить абсолютный путь к своей директории

    :param _file: Путь
    :param back: Сколько отступить назад
    """
    res = Path(_file).resolve()
    for _ in range(back):
        res = res.parent
    return res


def read_file_by_module(_path: str) -> ModuleType:
    """
    Импортировать файл как модуль `python`

    :param _path: Путь к `python` файлу
    :return: Модуль `python`
    """
    # Если не нужно проверять имя расширения
    if splitext(_path)[1] != ".py":  # Проверяем расширение файла
        raise ValueError(f"Файл должен иметь расширение .py")
    # указать модуль, который должен быть импортируется относительно пути модуль
    spec: Optional[ModuleSpec] = importlib.util.spec_from_file_location("my_module", _path)
    # создает новый модуль на основе спецификации
    __module: ModuleType = importlib.util.module_from_spec(spec)
    # выполняет модуль в своем собственном пространстве имен,
    # когда модуль импортируется или перезагружается.
    spec.loader.exec_module(__module)
    return __module



