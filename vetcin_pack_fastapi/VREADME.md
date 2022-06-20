# Быстрый старт

- Проект
    - static
        - css
        - js
    - main.py
    - settings.py
    - user
        - api.py
        - model.py

- main.py

```python
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from settings import Settings
from vetcin_pack_fastapi.manage_logic import Mange, allow_command

app = FastAPI(version="1.3", default_response_class=ORJSONResponse)

mg = Mange(app, Settings)

if __name__ == '__main__':
    mg.run_command(allow_command.run_dev)
```

- settings.py

```python
"""
Файл настроек проекта
"""
from pathlib import Path

from vetcin_pack_fastapi.database_pack.base import SqlUrlConnect
from vetcin_pack_fastapi.mount_logic import BaseMount
from vetcin_pack_fastapi.settings_logic import AllowedNamesTypeFromSettings


class Settings(AllowedNamesTypeFromSettings):
    """
    БД
    """
    # Url подключения к БД "postgresql+asyncpg://postgres:root@localhost/fast"
    SQLALCHEMY_DATABASE_URL = SqlUrlConnect.postgresql('denis', '123', 'localhost', 'market')
    """
    Пути
    """
    # Полный путь к приложению
    BASE_DIR = Path(__file__).resolve().parent
    # Полный путь к проекту
    ROOT_DIR = Path(__file__).resolve().parent.parent
    # Путь к папке со стоическими файлами
    STATIC_PATH = BASE_DIR / "static"
    """
    Статические файлы
    """

    """
    Админ панель
    """
    # Имя админа
    ADMIN_USER_NAME = "denis"
    # Пароль от админ панели
    ADMIN_PASSWORD = "321"
    """
    Сервер
    """
    # Порт сервера
    PORT_WEB = 8001
    # IP сервера
    HOST_WEB = "127.0.0.1"

    class Mount(BaseMount):
        """
        Монтирование зависимостей
        """

        def mount_app(self):
            import users.api
            import users.model
            self.add_app(
                name="user",
                route=users.api.router,
                model=[users.model.User],
                static=users
            )
            import vetcin_pack_fastapi.session_pack.api
            self.add_app(name="session_pack", route=vetcin_pack_fastapi.session_pack.api.router)
```

- user/api.py

```python
from fastapi import APIRouter, Response

router = APIRouter(tags=["user"], prefix="/user")


@router.get("/register")
async def register(
        response: Response,
):
    """Зарегистрировать нового пользователя"""
    return {"message": "Привет пользователь"}
```

- user/model.py

```python
from vetcin_pack_fastapi.database_pack.model_logic import RawSqlModel


class User(RawSqlModel):
    table_name = 'user'

    @staticmethod
    def create_table() -> str:
        return """
    create table users2
    (
        id              serial
            constraint users_pkey2
                primary key,
        email           varchar not null,
        hashed_password varchar not null,
        token           varchar,
        is_active       boolean not null
    );
    """
```

# Правильная структура проекта

## Схема

- Проект
    - static
        - css
        - js
    - main.py
    - settings.py
    - приложение_1
        - static
            - css
                - main.css
            - js
                - main.js
        - template
            - index.html
        - app.py
        - model.py

## Описание содержания фала

- main.py

```python

```

- settings.py

```python

```