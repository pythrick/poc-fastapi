from uuid import UUID

from pydantic.main import BaseModel


class UserSchema(BaseModel):
    uuid: UUID
    username: str

    class Config:
        orm_mode = True


class UserInSchema(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
