# Как пользоваться пакетом `vetcin_pack_fastapi`

1. В проекте нужно создать файл `settings.py` в которому будут указаны данные для переменных окружения, эти переменные
   будут использоваться во многих участках программы, а также подключение утилит.

2. Для выполнения заранее подготовленных сценариев, например как запуск сервера, создание таблиц на основе подключенных
   моделей, и др. нужно создать файл `main.py`.

# Эталонная структура проекта

- Проект
  - static [+](IREADME.md#main%20py%20Как%20происходит%20подключение%20различных%20утилит%20к%20проекту)
    - приложение_N [+](#create_app%20Добавить%20новое%20приложение%20в%20проект)
      - css
      - js
  - main.py [+](IREADME.md#main%20py%20Как%20происходит%20подключение%20различных%20утилит%20к%20проекту)
  - settings.py [+](#settings%20py%20Общие%20настройки%20проекта)
  - приложение_N [+](#create_app%20Добавить%20новое%20приложение%20в%20проект)

# `settings.py` Общие настройки проекта

Это основной и обязательный файл для хранения настроек проекта. Если вам нужно хранить все настройки в файле в
формате `.env`, то тогда импортируйте их в `settings.py` через готовую
функцию `vetcin_pack_fastapi.settings_logic.read_env_file('ПутьEnvФайлу')->dict[ИмяКлюча,Значение]`

В файле `settings.py` нужно создать класс например назвать его `Settings`, который наследуется
от `vetcin_pack_fastapi.settings_logic.BaseSettings`. В `BaseSettings` указаны обязательные(используются в логики
библиотеки) и необязательные(по опыту часто используемые) атрибуты класс наследника, соответственно обязательные
атрибуту нужно заполнить в классе наследнике.

Вот пример шаблона `Проект/settings.py`

```python
"""
Файл настроек проекта
"""
from pathlib import Path

from vetcin_pack_fastapi.database_pack.base import SqlUrlConnect
from vetcin_pack_fastapi.mount_logic import BaseMount
from vetcin_pack_fastapi.settings_logic import BaseSettings


class Settings(BaseSettings):
    """Пути"""
    #: Полный путь к проекту FASTAPI
    BASE_DIR: Path = Path(__file__).resolve().parent
    #: Полный путь к проекту (на 1 уровень выше)
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent
    #: Путь к папке со статическими файлами
    #: FastApi будет маршрутизировать папку со статическими файлами,
    #: если вы хотите это делать с помощью Nginx то установите пустую строку ''
    STATIC_PATH: Path = BASE_DIR / "static"
    """БД"""
    #: Url подключения к БД ``СУБД+ДРАЙВЕР://USER:PASSWORD@HOST:PORT/ИМЯ_БД``
    SQLALCHEMY_DATABASE_URL: str = SqlUrlConnect.postgresql('USER', 'PASSWORD', 'HOST', 'ИМЯ_БД')
    """Сервер"""
    #: На коком хосту запустить веб сервер
    HOST_WEB: str = "0.0.0.0"
    #: На коком порту запустить веб сервер
    PORT_WEB: int = "8080"
    #: Авто перезагрузка сервера
    RELOAD_WEB: bool = True
    """Отчетность"""
    #: Все добавленные приложения
    ALL_APP: str = ""
    #: Все добавленные SQL модели
    ALL_MODEL: str = ""

    class Mount(BaseMount):
        """
        Монтирование зависимостей
        """

        def mount_app(self):
            """
            Подключение приложений
            """
            import Приложение.api
            import Приложение.model
            self.add_app(
                name="ИмяПриложения",
                route=Приложение.api.router,
                model=[Приложение.model.ИмяМодели],
            )
            import vetcin_pack_fastapi.session_pack.api
            self.add_app(name="session_pack", route=vetcin_pack_fastapi.session_pack.api.router)
```

# `main.py` Как происходит подключение различных утилит к проекту

1. Начала взаимодействия с пакетом начинается при создании объекта `Mange`

```python
from fastapi import FastAPI
from settings import Settings
from vetcin_pack_fastapi.manage_logic import Mange, allow_command

app = FastAPI()
mg = Mange(app, Settings)

if __name__ == '__main__':
   mg.run_command(allow_command.run_dev)
```

Здесь мы создаем объект `Mange` и передаем в параметры (основное приложение `app`, и объект с настройками `Settings`).
Переменная в которую присваивается это объект нужно назвать `mg`, это нужно для работы консольных команд.

Основные этапы которые происходят при создании объекта `Mange` (\* именно в таком порядке):

1. Прочитать атрибуты класса `Settings` и занести их в переменные окружения.
2. Создать подключение к СУБД на основе атрибута `Settings.SQLALCHEMY_DATABASE_URL`.
3. Подключить `URL` пути к основному приложению. Рекомендую назвать файл `api.py` в нем должен быть создан
   объект `fastapi.APIRouter`
   например `router = APIRouter(tags=["ИмяТега"], prefix="/ПрефиксДляСылки")`
4. Подключить `SQL` модели к проекту. Рекомендую назвать файл `model.py` в нем должны быть модели которые наследуются
   от `SQL.Base` или `RawSqlModel`, можно иметь оба варианта сразу.
5. Подключить статические файлы к проекту. Для этого нужно иметь папку `static` в корне проекта.
   Например `ИмяПроекта/static/`.

# Консольные команды

Проверить доступность файла который реализует логику выполнения консольных команд

```bash
python -m vetcin_pack_fastapi.console_logic --help
```

Если библиотека находится вне `sys.path`, то перед выполнением команды укажите полный путь к ней в `PYTHONPATH`

```bash
PYTHONPATH=/ПолныйПуть/vetcin_pack_fastapi python -m vetcin_pack_fastapi.console_logic --help
```

## `run_dev` Запустить сервер

```bash
python -m vetcin_pack_fastapi.console_logic run_dev main.py
```

## `create_app` Добавить новое приложение в проект

Для того чтобы создать новое приложение на основе стандартного шаблона, нужно выполнить команду. НЕЗУБУДТЕ добавить новое приложение в `settings.py->Settings->Mount->mount_app`

```bash
python -m vetcin_pack_fastapi.console_logic create_app main.py -n НовоеИмяПриложения
```

В итоге будет следующая структура проекта

- Проект

  - НовоеИмяПриложения

    - templates (Папка для `Html` файлов)
    - api.py (Папка для `url` маршрутизаторов)
    - base.py (Папка с основной логикой приложения)
    - helpful.py (Утилиты для приложения)
    - model.py (Модели `SQL`) [+](IREADME.md#SQL%20Модели)

            ```python
            from vetcin_pack_fastapi.database_pack.model_logic import RawSqlModel, SqlTypeReturn

            class ИмяМодели(RawSqlModel):
                table_name = 'ИмяМодели'

                @classmethod
                def create_table(cls) -> SqlTypeReturn:
                    return SqlTypeReturn(
                        raw_sql="""
                        create table if not exists :table_name
                        (
                            id             serial primary key
                        );
                        """,
                        params={"table_name":cls.table_name}
                    )
            ```

    - model_logic.py (Реализация `SQL` запросов к `СУБД` для моделей из файла `model.py`) [+](IREADME.md#SQL%20Модели)

            ```python![](../../../../../../home/denis/Рабочий стол/13.jpg)
            from НовоеИмяПриложения.model import ИмяМодели![](../../../../../../home/denis/Рабочий стол/13.jpg)

            class ИмяМоделиLogic(ИмяМодели):
                ...

            ```

    - schema.py (`JSON` схемы на основе библиотеки `Pydantic`)

## `init_models` Создание моделей в БД

Те модели которые подключены к проекту в `Mount.mount_app` через метод `self.add_app(...,model=[Модель_N])` будут участвовать в выполнение команды.

Очередность команды можно посмотреть в `/vetcin_pack_fastapi/manage_base.py : BaseManage.init_models`.

## `delete_models` Удаление моделей из БД

Те модели которые подключены к проекту в `Mount.mount_app` через метод `self.add_app(...,model=[Модель_N])` будут участвовать в выполнение команды.

Очередность команды можно посмотреть в `/vetcin_pack_fastapi/manage_base.py : BaseManage.delete_models`.

# `SQL` Модели

Для организованного и структурированного использование `СУБД` предполагается следующая логика. В каждом приложение есть свой файл `model.py` в котром вы объявляете таблицы.

Теоретические наставления что конкретно что должны быть в объявление модели таблицы (звездочка \* значит необязательно):

- Имя таблицы
- Метод для создания таблицы в `СУБД`
- \* Метод для удаления таблицы из `СУБД`
- \* Данные которые нужно внести в таблицу единожды после её создания

В итоге файл `model.py` должен давать общий взгляд, на то какие таблицы есть в приложение, а реализацию `SQL` запросов нужно писать в файле `model_logic.py`. При таком варианте логично в файле `model.py` создавать класс например `class User():` а в файле `model_logic.py` наследоваться от этого класса и назвать его `class UserLogic(User):`

## Вариант модели через `RawSqlModel`

Сырые `SQL` запросы дают большую гибкость в использование БД, они дают возможность пользоваться всеми особенностями `СУБД`. Для унификации моделей ориентированных на использование сырых `SQL` запросов, есть класс `vetcin_pack_fastapi.database_pack.model_logic.RawSqlModel`, от этого класса должна наследоваться наша модель `class ИмяМодели(RawSqlModel)`.

В наследнике `RawSqlModel` можно реализовать методы:

- `create_table()` Выполняется при команде [init_models](IREADME.md#init_models%20Создание%20моделей%20в%20БД)
- `drop_table()` Выполняется при команде [delete_models](IREADME.md#delete_models%20Удаление%20моделей%20из%20БД)
- `init_data()` Выполняется при команде [init_models](IREADME.md#init_models%20Создание%20моделей%20в%20БД) после метода `create_table()`

И атрибут:

- `table_name` Имя таблицы, которое вы можете использовать в сырых `SQL` запросах.

---

Пример реализации модели в `model.py` через `RawSqlModel`

```python
from vetcin_pack_fastapi.database_pack.model_logic import RawSqlModel


class User(RawSqlModel):
    table_name = 'users'

    @classmethod
    def create_table(cls) -> str:
        return f"""
    create table if not exists  {cls.table_name}
    (
        id              serial primary key,
        Surname         varchar(255) not null,
        Firstname       varchar(255) not null,
        Midname         varchar(255),
        login           varchar(255) unique not null,
        date_birth      date not null,
        phone           varchar(10) unique,
        HASH_PASWORD    varchar(255) not null,
        is_admin        smallint not null
    );
    """

    @classmethod
    def init_data(cls) -> str:
        return """INSERT INTO public.users (id, surname, firstname, midname, login, date_birth, phone, hash_pasword, is_admin) VALUES (1, 'Иванов', 'Иван', 'Иванович', 'ivan1', '1991-06-01', '8123456789', '3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2', 1);"""

    @classmethod
    def drop_table(cls) -> str:
        return f"""drop table {cls.table_name}"""
```

Пример реализации логики модели в `model_logic.py`. `SqlTypeReturn` это шаблонный словарь на основе `typing.TypedDict`

```python
from .model import User
from vetcin_pack_fastapi.database_pack.model_logic import SqlTypeReturn


class UserLogic(User):

    @classmethod
    def login(cls, login: str, password: str) -> SqlTypeReturn:
        return SqlTypeReturn(
            raw_sql=f"""
          select id
    from {cls.table_name}
    where login = :login and hash_pasword = :hash_pasword
    """,
            params={"login": login, "hash_pasword": password}
        )
```

Пример использования в `api.py`

```python
from fastapi import Request, Response, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from vetcin_pack_fastapi.database_pack.base import SQL
from vetcin_pack_fastapi.database_pack.helpful import hashPassword
from vetcin_pack_fastapi.http_helpful import ErrorCode, error_json, successfully_json
from .model_logic import UserLogic


class loginSchema(BaseModel):
    login: str
    password: str


@router.api_route("/api/login", methods=["POST"])
async def login(
        request: Request,
        response: Response,
        schema: loginSchema,
        session: AsyncSession = Depends(SQL.get_session),
):
    """Войти в аккаунт пользователя"""
    res = await SQL.read_execute_raw_sql(session, **UserLogic.login(schema.login, hashPassword(schema.password)))
    if res:
        res_id = int(res[0]['id'])
        return successfully_json({"id": res_id})
    else:
        return error_json("Пользователь не найден", ErrorCode._1)
```
