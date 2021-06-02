from dataclasses import dataclass, field

from fastapi import HTTPException, status


@dataclass
class InternalServerError(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Internal server error."


@dataclass
class InvalidPassword(HTTPException):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail: str = "Wrong password"


@dataclass
class UserAlreadyExists(HTTPException):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail: str = "Unavailable username"


@dataclass
class InvalidCredentials(HTTPException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Could not validate credentials"
    headers: dict = field(default_factory=lambda: {"WWW-Authenticate": "Bearer"})


@dataclass
class UserNotFound(HTTPException):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "User not found"
