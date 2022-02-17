from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from fast_xabhelper.database_pack.castom_sql_type import ImageField
from fast_xabhelper.database_pack.database import Base


class Photo(Base):
    __tablename__ = "photo"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    path = Column(ImageField(400), nullable=False, index=True)

    user = relationship("User", backref="photo")

    def __repr__(self):
        return f"{self.id}:{self.path}"
