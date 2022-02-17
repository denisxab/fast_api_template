from typing import Any

from sqlalchemy.sql.type_api import TypeEngine

CONVERT_SQL_TYPE_TO_HTML_INPUT_TYPE: dict[str, str] = {
    'INTEGER': "number",
    "VARCHAR": "text",
    "BOOLEAN": "radio"
}

Convert_sql_type_to_python_type: dict[str, Any] = {
    'INTEGER': int,
    "VARCHAR": str,
    "BOOLEAN": bool,
}

Convert_html_input_type_to_python_type: dict[str, Any] = {
    "number": int,
    "text": str,
    "radio": lambda _data: True if _data == "on" else False
}


def convert_sql_type_to_html_input_type(sql_type: TypeEngine):
    """
    Конвертировать SQL тип в HTML INPUT

    @param sql_type:
    """
    return CONVERT_SQL_TYPE_TO_HTML_INPUT_TYPE.get(str(sql_type), None)


def convert_html_input_type_to_python_type(form_html: dict[str, str]) -> dict[str, Any]:
    """
    Конвертировать HTML INPUT тип в Python тип

    @param form_html: Словарь ключ `имя-html_тип` значение `строка`
    """
    res: dict[str, Any] = {}
    for _k, _v in form_html.items():
        # Отделяем имя от типа
        name, type_ = _k.split("-")
        # Получим функцию для конвертации
        type_ = Convert_html_input_type_to_python_type[type_]
        # Конвертируем значения
        res[name] = type_(_v)
    return res
