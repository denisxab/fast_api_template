# class PathField(String):
#
#     # def __init__(self):
#     #     TypeEngine().__init__(self,)
#     # self.type = "PathField"
#
#     # def compile(self, dialect=None):
#     #     super().compile(self, dialect)
#     #     return "PathField"
#
#     # Переопределить возвращаемый тип
#     def __str__(self):
#         return f"PathField({self.length})"
#


from sqlalchemy import String
from sqlalchemy.types import TypeDecorator


class PathField(TypeDecorator):
    impl = String

    cache_ok = True

    def __init__(self, length=None, *args, **kwargs):
        super().__init__(length, *args, **kwargs)

    def __str__(self):
        return f"PathField"


class ImageField(PathField):

    def __str__(self):
        return f"ImageField"
