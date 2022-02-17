from sqlalchemy import String


class PathField(String):
    # Переопределить возвращаемый тип
    def __str__(self):
        return f"PathField({self.length})"


class ImageField(PathField):
    # Переопределить возвращаемый тип
    def __str__(self):
        return f"ImageField({self.length})"
