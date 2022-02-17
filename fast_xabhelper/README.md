# Запустить проект

```python
from fastapi import FastAPI

from fast_xabhelper.manage import Mange
from mount import Mount

app = FastAPI()

mg = Mange(Mount, app)
# Настраиваем проект
mg.main("init")

if __name__ == "__main__":
    # Запускаем проект
    mg.main("run_dev")
```

# Создать настройки

По умолчанию настройки ищутся по пути `./settings.py`. Вам нужно создать переменные. Со всеми доступными переменными
можно познакомиться в `settings_logic.AllowedNamesType`. Которые будет прочитанные и занесены в переменные окружения
интерпретатора.

# Создать файл монтирования

Все подключения должны производиться в файле `mount.py` для этого нужно реализовать логику класса `BaseMount`

Вы можете примонтировать:

- `mount_route()` - пути, для этого используйте функцию `add_route()`.
- `mount_model()` - модели `SqlAlchemy`, для этого используйте функцию `add_model()`.
- `mount_admin_panel()` - админ панели, `Admin.add_panel()`.
- `mount_static()` - статические файлы.
- `mount_other_dependents()` - Что нибудь другое.