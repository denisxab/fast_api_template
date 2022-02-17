"""
Файл для подключения зависимостей к приложению
"""

from fastapi.staticfiles import StaticFiles

import api
import fast_xabhelper.admin_pack.fast_admin
import fast_xabhelper.session_pack.fast_session
import fast_xabhelper.user_pack.fast_user
from admin import UserPanel
from fast_xabhelper.admin_pack.admin_base import Admin
from fast_xabhelper.helpful import add_route


def on_startup_mount(app):
    """
    При старте подключить зависимости
    """

    @app.on_event("startup")
    async def on_startup():
        """
        Задачи которы нужно выполнить при запуске сервера
        """
        # Примонтировать зависимости
        mount_dependents()


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
    add_route(app, fast_xabhelper.user_pack.fast_user.router,
              name="user_pack")
    add_route(app, fast_xabhelper.session_pack.fast_session.router,
              name="session_pack")
    add_route(app, api.router,
              name="api")
    add_route(app, fast_xabhelper.admin_pack.fast_admin.router,
              path_static="/home/denis/PycharmProjects/fastApiProject/fast_xabhelper/admin_pack/static/", absolute=True,
              name="admin_pack")
    """
    Подключаем таблицу к админ панели
    """
    Admin.append_panel(UserPanel())
