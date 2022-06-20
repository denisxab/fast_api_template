"""
Файл для взаимодействия с пользователем через терминальные команды
"""
from os.path import splitext
from sys import path

from click import Path, argument, Choice, echo, command, option

from .helpful import absolute_path_dir, read_file_by_module
from .manage_logic import allow_command


@command()
@argument('cmd', nargs=1, type=Choice(allow_command.__members__))
@argument('path_where_app', nargs=1, type=Path(exists=True, dir_okay=False))
@option("manage_name", "--manage-name", '-mn', default="mg", type=str)
@option("name_app", "--name-app", '-n', default="", type=str)
def run_command(cmd, path_where_app, manage_name, name_app):
    """
    Выполнить команду

    @param cmd: Команда
    @param path_where_app: Путь для приложения
    @param manage_name: Имя экземпляра `Mange()`
    @param name_app:

    :Пример использования:
    ..code-block::bash
        python  -m vetcin_pack_fastapi.console_logic run_dev main.py
    """
    echo(f"{cmd=}")

    # Проверяем расширение файла
    if splitext(path_where_app)[1] != ".py":
        raise ValueError(f"Файл `{path_where_app}` должен иметь расширение .py")

    # Добавить свой путь `vetcin_pack_fastapi`
    path.append(str(absolute_path_dir(__file__, 2)))
    # Добавить путь к проекту
    path.append(str(absolute_path_dir(path_where_app)))

    # Импортируем `main.py` и берем из него экземпляр `Mange`
    __module = read_file_by_module(path_where_app)
    mg = __module.__dict__[manage_name]

    match cmd:
        # Создать шаблонное приложение
        case allow_command.add_app.name:
            if not name_app:
                raise ValueError(f"Аргумент `name_app` не задан !")
            else:
                mg.run_command(allow_command[cmd], name_app=name_app)
        # Запустить сервер
        case allow_command.run_dev.name | allow_command.init_models.name:
            mg.run_command(allow_command[cmd])


if __name__ == '__main__':
    run_command()
