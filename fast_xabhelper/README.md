# Запустить проект

Шаблон `main.py`

```python
from fastapi import FastAPI

from fast_xabhelper.manage_logic import Mange, comd
from settings import Mount

app = FastAPI()

mg = Mange(Mount, app)
# Настраиваем проект
mg.run_command(comd.init_app)

if __name__ == "__main__":
    # Запускаем проект
    mg.run_command(comd.run_dev)
```

Или вы можете запустить сервер командой

```bash
python fast_xabhelper/console_manage.py run_dev project_name/main.py
```

# Сценарии запуска

Для того чтобы посмотреть доступные команды введите

```bash
python fast_xabhelper/console_manage.py --help
```

# Настройки

## Создать настройки

По умолчанию настройки ищутся по пути `./settings.py`. Вам нужно создать переменные. Со всеми доступными переменными
можно познакомиться в `settings_logic.AllowedNamesType`. Которые будет прочитанные и занесены в переменные окружения
`Python` интерпретатора.

## Монтирование всего и вся

Все подключения должны производиться в файле настроек `./settings.py` для этого нужно реализовать логику
класса `BaseMount`

Вы можете примонтировать:

- `mount_route()` - пути, для этого используйте функцию `add_route()`.
- `mount_model()` - модели `SqlAlchemy`, для этого используйте функцию `add_model()`.
- `mount_admin_panel()` - админ панели, `Admin.add_panel()`.
- `mount_static()` - статические файлы.
- `mount_other_dependents()` - Что нибудь другое.
- `mount_src_svelte()` - Подключить скрипты `Svelte`