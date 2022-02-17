"""
Файл для подключения зависимостей к приложению
"""

from fastapi.staticfiles import StaticFiles

import api
import fast_xabhelper.admin_pack.fast_admin
from fast_xabhelper.helpful import add_route


def mount_dependents():
    """
    Подключение зависимостей к приложению
    """
    from app import app
    """
    Подключение статических файлов
    """
    app.mount(
        # `URL` путь
        "/static",
        # Директория в которой искать статические файлы
        StaticFiles(directory="static"),
        # Это имя будем использовать в
        # `{{ url_for('$name$', path='/$Файл$.css') ) }}`
        name="static")

    """
    Подключение путей к приложению
    """
    add_route(app, api.router, name="api")
    add_route(app, fast_xabhelper.admin_pack.fast_admin.router,
              name="admin_pack",
              path_static="/home/denis/PycharmProjects/fastApiProject/fast_xabhelper/admin_pack/static/", absolute=True)
