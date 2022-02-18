from sqlalchemy import String


class PathField(String):

    # def __init__(self):
    #     TypeEngine().__init__(self,)
    # self.type = "PathField"

    # def compile(self, dialect=None):
    #     super().compile(self, dialect)
    #     return "PathField"

    # Переопределить возвращаемый тип
    def __str__(self):
        return f"PathField({self.length})"


class ImageField(PathField):
    # Переопределить возвращаемый тип
    def __str__(self):
        return f"ImageField({self.length})"
