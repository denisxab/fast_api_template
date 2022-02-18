"""
Файл настроек проекта
"""
from pathlib import Path

from fast_xabhelper.helpful import add_route, add_model
from fast_xabhelper.mount_logic import BaseMount

"""
БД
"""
# Url подключения к БД "postgresql+asyncpg://postgres:root@localhost/fast"
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost/fast"
"""
Пути
"""
# Полный путь к Django приложению
BASE_DIR = Path(__file__).resolve().parent
# Полный путь к проекту
ROOT_DIR = Path(__file__).resolve().parent.parent
# Путь к папке со стоическими файлами
STATIC_PATH = BASE_DIR / "static"
"""
Статические файлы
"""
# Нудно ли копировать статические файлы
COPY_STATIC = "True"
"""
Админ панель
"""
# Имя админа
ADMIN_USER_NAME = "denis"
# Пароль от админ панели
ADMIN_PASSWORD = "321"


class Mount(BaseMount):
    """
    Монтирование зависимостей
    """

    def mount_route(self):
        import fast_xabhelper.admin_pack.fast_admin
        import fast_xabhelper.session_pack.fast_session
        import fast_xabhelper.user_pack.fast_user
        add_route(self.app, fast_xabhelper.user_pack.fast_user.router,
                  name="user_pack")
        add_route(self.app, fast_xabhelper.session_pack.fast_session.router,
                  name="session_pack")
        add_route(self.app, fast_xabhelper.admin_pack.fast_admin.router,
                  path_static="/home/denis/PycharmProjects/fastApiProject/fast_xabhelper/admin_pack/static/",
                  absolute=True,
                  name="admin_pack")

    def mount_model(self):
        from fast_xabhelper.user_pack.model import User
        from photo.model import Photo
        add_model(Photo)
        add_model(User)

    def mount_admin_panel(self):
        from fast_xabhelper.admin_pack.admin_base import Admin
        from fast_xabhelper.user_pack.admin import UserPanel
        from photo.admin import PhotoPanel
        Admin.add_panel(UserPanel())
        Admin.add_panel(PhotoPanel())
