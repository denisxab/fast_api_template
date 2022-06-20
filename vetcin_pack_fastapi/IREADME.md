# Как пользоваться пакетом `vetcin_pack_fastapi`

1. В проекте нужно создать файл `settings.py` в которому будут указаны данные для переменных окружения, эти переменные
   будут использоваться во многих участках программы, а также подключение утилит. Шаблон для `settings.py` смотрите
   в `VREADME.md/Правильная структура проекта`

2. Для выполнения заранее подготовленных сценариев, например как запуск сервера, создание таблиц на основе подключенных
   моделей, и др. нужно создать файл `main.py`. Шаблон для `settings.py` смотрите
   в `VREADME.md/Правильная структура проекта`

# `settings.py` Общие настройки проекта

Это основной и обязательный файл для хранения настроек проекта. Если вам нужно хранить все настройки в файле в
формате `.env`, то тогда импортируйте их в `settings.py` через готовую
функция `vetcin_pack_fastapi.settings_logic.read_env_file('ПутьEnvФайлу')->dict[ИмяКлюча,Значение]`

В файле `settings.py` нужно создать класс например назовем его `Settings`, который наследуется
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

# Как происходит подключение различных утилит к проекту

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

Основные этапы которые происходят при создании объекта `Mange` (* именно в таком порядке):

1. Прочитать атрибуты класса `Settings` и занести их в переменные окружения.
2. Создать подключение к СУБД на основе атрибута `Settings.SQLALCHEMY_DATABASE_URL`.
3. Подключить `URL` пути к основному приложению. Рекомендую назвать файл `api.py` в нем должен быть создан
   объект `fastapi.APIRouter`
   например `router = APIRouter(tags=["ИмяТега"], prefix="/ПрефиксДляСылки")`
6. Подключить `SQL` модели к проекту. Рекомендую назвать файл `model.py` в нем должны быть модели которые наследуются
   от `SQL.Base` или  `RawSqlModel`, можно иметь оба варианта сразу.
7. Подключить статические файлы к проекту. Для этого нужно иметь папку `static` в корне проекта.
   Например `ИмяПроекта/static/`.

# Консольные команды

Проверить доступность файла который реализует логику выполнения консольных команд

```bash
python -m vetcin_pack_fastapi.console_logic --help
```

Если библиотека находится вне `sys.path`, то перед выполнением команды укажите полный путь к ней в  `PYTHONPATH`

```bash
PYTHONPATH=/ПолныйПуть/vetcin_pack_fastapi python -m vetcin_pack_fastapi.console_logic --help
```

## `create_app` Добавить новое приложение в проект

Для того чтобы создать новое приложение на основе стандартного шаблона, нужно выполнить команду

```bash
python -m vetcin_pack_fastapi.console_logic create_app mani.py -n НовоеИмяПриложения
```

В итоге будет следующая структура проекта

- Проект
    - НовоеИмяПриложения
        - templates (Папка для `Html` файлов)
        - api.py (Папка для `url` маршрутизаторов)
        - base.py (Папка с основной логикой приложения)
        - helpful.py (Утилиты для приложения)
        - model.py (Модели `SQL`)
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
        - model_logic.py (Реализация `SQL` запросов к `СУБД` для моделей из файла `model.py`)
            ```python
            from НовоеИмяПриложения.model import ИмяМодели
            
            class ИмяМоделиLogic(ИмяМодели):
                ...
                    
            ```
        - schema.py (`JSON` схемы на основе библиотеки `Pydantic`)






