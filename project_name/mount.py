from fastapi.staticfiles import StaticFiles

from fast_xabhelper.helpful import add_route, add_model
from fast_xabhelper.mount_logic import BaseMount


class Mount(BaseMount):
    """
    Монтирование зависимостей
    """

    @staticmethod
    def mount_route(_app):
        import api
        import fast_xabhelper.admin_pack.fast_admin
        import fast_xabhelper.session_pack.fast_session
        import fast_xabhelper.user_pack.fast_user
        add_route(_app, fast_xabhelper.user_pack.fast_user.router,
                  name="user_pack")
        add_route(_app, fast_xabhelper.session_pack.fast_session.router,
                  name="session_pack")
        add_route(_app, api.router,
                  name="api")
        add_route(_app, fast_xabhelper.admin_pack.fast_admin.router,
                  path_static="/home/denis/PycharmProjects/fastApiProject/fast_xabhelper/admin_pack/static/",
                  absolute=True,
                  name="admin_pack")

    @staticmethod
    def mount_model():
        from fast_xabhelper.user_pack.model import User
        from photo.model import Photo
        add_model(Photo)
        add_model(User)

    @staticmethod
    def mount_static(_app):
        _app.mount(
            # `URL` путь
            "/static",
            # Директория в которой искать статические файлы
            StaticFiles(directory="static"),
            # Это имя будем использовать в
            # `{{ url_for('$name$', path='/$Файл$.css') ) }}`
            name="static")

    @staticmethod
    def mount_admin_panel():
        from fast_xabhelper.admin_pack.admin_base import Admin
        from fast_xabhelper.user_pack.admin import UserPanel

        Admin.append_panel(UserPanel())
