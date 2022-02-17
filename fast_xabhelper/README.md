# Запустить проект

```python
from fastapi import FastAPI

from fast_xabhelper.manage import Mange, comd
from settings import Mount

app = FastAPI()

mg = Mange(Mount, app)
# Настраиваем проект
mg.run_command(comd.init_app)

if __name__ == "__main__":
    # Запускаем проект
    mg.run_command(comd.run_dev)
```

```bash
python fast_xabhelper/console_manage.py run_dev  project_name/main.py
```

# Создать настройки

По умолчанию настройки ищутся по пути `./settings.py`. Вам нужно создать переменные. Со всеми доступными переменными
можно познакомиться в `settings_logic.AllowedNamesType`. Которые будет прочитанные и занесены в переменные окружения
интерпретатора.

# Создать файл монтирования

Все подключения должны производиться в файле настроек `./settings.py` для этого нужно реализовать логику
класса `BaseMount`

Вы можете примонтировать:

- `mount_route()` - пути, для этого используйте функцию `add_route()`.
- `mount_model()` - модели `SqlAlchemy`, для этого используйте функцию `add_model()`.
- `mount_admin_panel()` - админ панели, `Admin.add_panel()`.
- `mount_static()` - статические файлы.
- `mount_other_dependents()` - Что нибудь другое.