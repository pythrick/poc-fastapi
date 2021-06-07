import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils.types.uuid import UUIDType


class BaseDB:
    non_editable_fields = ()
    default_non_editable_fields = ("id", "created_at", "updated_at")

    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, autoincrement=True)

    @declared_attr
    def uuid(cls):
        return Column(
            UUIDType(binary=False),
            unique=True,
            nullable=False,
            index=True,
            default=uuid.uuid4,
        )

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.utcnow)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, onupdate=datetime.utcnow)

    def __str__(self):
        return str(self.uuid)

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"
