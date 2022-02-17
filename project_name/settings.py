"""
Файл настроек проекта
"""
from pathlib import Path

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
ROOT_DIR = "/".join(str(BASE_DIR).split('/')[:-1])
"""
Статические файлы
"""
COPY_STATIC = "False"
# Нудно ли копировать статические файлы
"""
Админ панель
"""
# Имя админа
ADMIN_USER_NAME = "denis"
# Пароль от админ панели
ADMIN_PASSWORD = "123"
"""
Все добавленные приложения
"""
ALL_APP = ""
