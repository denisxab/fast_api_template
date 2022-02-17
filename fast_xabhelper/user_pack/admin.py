"""
Файл для отображения модели в админ панели
"""

from fast_xabhelper.admin_pack.admin_base import AdminPanel
from fast_xabhelper.user_pack.model import User


class UserPanel(AdminPanel):
    name = "Юзеры"
    model = User
    list_display = ["id", "email", "is_active"]
