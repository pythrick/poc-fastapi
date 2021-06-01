from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from poc_fastapi.db.base import Base
from poc_fastapi.models.base import BaseDB


class Post(BaseDB, Base):
    __tablename__ = "posts"

    content = Column(String(280), nullable=False, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="posts")
