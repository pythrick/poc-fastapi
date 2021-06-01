from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from poc_fastapi.schemas.user import UserSchema


class PostInSchema(BaseModel):
    content: str


class PostSchema(BaseModel):
    uuid: UUID
    content: str
    owner: UserSchema
    created_at: datetime

    class Config:
        orm_mode = True
