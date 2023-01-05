"""
Файл для общих функций управления проекта
"""
import os.path
from os import environ
from typing import Type

from fastapi import FastAPI
from logsmal import logger
from sqlalchemy.exc import DatabaseError

from mg_sql.sql_async.base import SQL
from mg_sql.sql_async.model_logic import RawSqlModel
from .helpful import create_file
from .settings_logic import BaseSettings, mount_env


class BaseManage:
    """
    Функции для менеджера проекта
    """

    def __init__(self, app: FastAPI, settings_obj: Type[BaseSettings]):
        self.settings_obj = settings_obj
        self.app = app
        self.include_settings()
        self.include_db()
        self.include_mount()

    def include_settings(self):
        """
        Подключить настройки проекта
        """
        #: 1. Подключаем переменные окружения из настроек проекта
        mount_env(self.settings_obj)

    def include_mount(self):
        """
        Подключаем зависимости приложения
        """
        self.settings_obj.Mount(self.app).run_mount()

    @staticmethod
    def include_db():
        """
        Подключить БД
        """
        SQL(environ['SQLALCHEMY_DATABASE_URL'])

    @staticmethod
    async def init_models():
        """
        Создать таблицы в БД, которые подключены к проекту
        """

        #  Создать таблицы который указаны через использование BaseMode из
        #  библиотеки SqlAlchemy
        if len(SQL.Base.metadata.tables) > 0:
            async with SQL.engine.begin() as conn:
                await conn.run_sync(SQL.Base.metadata.create_all)
            logger.info(f"Таблицы созданы {list(SQL.Base.metadata.tables.keys())}")
        # Создать таблицы которые указаны через наследование `RawSqlModel`
        if RawSqlModel.all_tables:
            for k, v in RawSqlModel.all_tables.items():
                v: RawSqlModel
                await SQL.execute_raw_sql(v.create_table())
                try:
                    if v.init_data():
                        await SQL.execute_raw_sql(v.init_data())
                except DatabaseError as e:
                    logger.warning(f"Ошибка инициализации данных:{e}", ['init_data'])
                logger.info(f"Таблица создана {k}", ['init_models'])

    @staticmethod
    async def delete_models():
        """
        Удалить таблицы из БД, которые подключены к проекту
        """
        if input("Вы действительно хотите удалить все таблицы ? Для подтверждения введите `YES`") == "YES":
            # Удаляем таблицы модели которых созданы через `BaseMode` из библиотеки SqlAlchemy
            if len(SQL.Base.metadata.tables) > 0:
                async with SQL.engine.begin() as conn:
                    await conn.run_sync(SQL.Base.metadata.drop_all())
                    logger.info(f"Таблицы удалены {list(SQL.Base.metadata.tables.keys())}", ['delete_models'])
            # Удаляем таблицы которые указаны через наследование `RawSqlModel`
            if RawSqlModel.all_tables:
                for k, v in RawSqlModel.all_tables.items():
                    v: RawSqlModel
                    await SQL.execute_raw_sql(v.drop_table())
                    logger.info(f"Таблица удалена {k}", ['delete_models'])
        else:
            logger.info("Таблицы НЕ удалены")

    @staticmethod
    def create_app(name_app: str):
        """
        Создать шаблон приложения

        :param name_app: Имя приложения

        - ИмяПриложения
            - template
            - api.py
            - base.py
            - model.py
            - model_logic.py
            - schema.py
            - helpful.py
        """
        # Путь для нового приложения
        path_app: str = os.path.join(environ['BASE_DIR'], name_app)
        # Создаем путь из папок к новому приложению
        os.makedirs(path_app, exist_ok=True)
        # Создаем папку с Html шаблонами
        os.makedirs(os.path.join(path_app, 'templates'), exist_ok=True)
        # Создаем шаблонные файлы в папке с новым приложением
        create_file(os.path.join(path_app, 'api.py'), """
from fastapi import APIRouter, Form, Response, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from mg_sql.sql_async.base import SQL
from vetcin_pack_fastapi.session_pack.base import SESSION_RAM

router = APIRouter(tags=["{name_app}"], prefix="/{name_app}")
name_app = "{name_app}"
        """[1:].format(name_app=name_app))
        create_file(os.path.join(path_app, 'base.py'))
        create_file(os.path.join(path_app, 'helpful.py'))
        create_file(os.path.join(path_app, 'model.py'), '''
from mg_sql.sql_async.model_logic import RawSqlModel, SqlTypeReturn

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
        '''[1:])
        create_file(os.path.join(path_app, 'model_logic.py'), '''
from {name_app}.model import ИмяМодели

class ИмяМоделиLogic(ИмяМодели):
    ...
        '''[1:].format(name_app=name_app))
        create_file(os.path.join(path_app, 'schema.py'))
        # Отчетность
        logger.info(path_app, ['CREATE_APP'])
