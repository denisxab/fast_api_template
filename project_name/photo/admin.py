from fast_xabhelper.admin_pack.admin_base import AdminPanel
from photo.model import Photo


class PhotoPanel(AdminPanel):
    name = "Фото"
    model = Photo
    list_display = ["id", "user_id", "path"]
