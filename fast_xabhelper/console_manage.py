"""
Файл для взаимодействия с пользователем через терминальные команды
"""
import sys
from os.path import splitext

import click
from mg_file.file.base_file import absolute_path_dir, read_file_by_module

from manage_logic import comd


@click.command()
@click.argument('path_where_app', nargs=1,
                type=click.Path(exists=True, dir_okay=False))
@click.argument('command', nargs=1, type=click.Choice(comd.__members__))
@click.option("manage_name", "--manage-name", '-mn', default="mg", type=str)
def run_command(command, path_where_app, manage_name):
    """
    Выполнить команду

    @param command: Команда
    @param path_where_app: Путь для приложения
    @param manage_name: Имя экземпляра `Mange()`
    """
    click.echo(f"{command=}")

    # Проверяем расширение файла
    if splitext(path_where_app)[1] != ".py":
        raise ValueError(f"Файл `{path_where_app}` должен иметь расширение .py")

    # Добавить свой путь `fast_xabhelper`
    sys.path.append(str(absolute_path_dir(__file__, 2)))
    # Добавить путь к проекту
    sys.path.append(str(absolute_path_dir(path_where_app)))

    # Импортируем `main.py` и берем из него экземпляр `Mange`
    __module = read_file_by_module(path_where_app)
    mg = __module.__dict__[manage_name]
    mg.run_command(comd[command])


if __name__ == '__main__':
    run_command()
