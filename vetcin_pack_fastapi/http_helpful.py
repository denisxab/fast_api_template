"""
Утилиты для работы с `HTTP`
"""
from enum import Enum


class ErrorCode(Enum):
    """
    Доступные коды ошибок и описание к ним

    Правило оформления нового кода ошибки: нижнее подчеркивание и цифра
    """
    _0 = 'Общая'
    _1 = 'Ошибка аутентификации'


def error_json(text: str, code: ErrorCode = ErrorCode._0) -> object:
    """
    Функция для `JSON` шаблона ошибки

    :param code: Код ошибки
    :param text: Текст ошибки
    """
    return {
        "status": "error",
        "body": {
            "error":
                {
                    "code": int(code.name.replace('_', '')), 'description': code.value, "text": text
                }
        }
    }


def successfully_json(obj: object = '') -> object:
    """
    Функция для `JSON` шаблона успешного выполнения

    :param obj: Любой объект
    """
    return {
        "status": "ok",
        "body": obj
    }
