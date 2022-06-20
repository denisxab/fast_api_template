# Картеж с именами аргументов, массив со значениями для аргументов
import pytest

from settings_logic import read_env_file


@pytest.mark.parametrize(("name_file", "true_res"), [
    ('test_env.env', {'DJANGO_SECRET_KEY': '{{secret_key}}', 'NAME_PROJ': '{{project_name}}', 'DEBUG': 'true',
                      'WORK_DIR': '/usr/src/{{project_name}}', 'PATH_ENV': './__env.env', 'EXTERNAL_WEB_PORT': '8081',
                      'NGINX_PORT': '8080', 'POSTGRES_DB': 'postgres', 'POSTGRES_USER': 'postgres',
                      'POSTGRES_PASSWORD': 'postgres', 'POSTGRES_HOST': 'db', 'POSTGRES_PORT': '5432',
                      'POSTGRES_VOLUMES': './db/pg_data'}),
])
def test_read_env_file(name_file: str, true_res: dict):
    res = read_env_file(name_file)
    assert res == true_res
