from passlib.context import CryptContext
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from poc_fastapi.db.base import Base
from poc_fastapi.exceptions import InvalidPassword
from poc_fastapi.models.base import BaseDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseDB, Base):
    __tablename__ = "users"

    username = Column(String(15), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    posts = relationship("Post", back_populates="owner")

    def set_password(self, plain_password: str):
        self.hashed_password = pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        if not pwd_context.verify(plain_password, self.hashed_password):
            raise InvalidPassword
        return True
