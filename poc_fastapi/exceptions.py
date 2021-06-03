from dataclasses import dataclass, field

from fastapi import HTTPException, status


@dataclass
class InternalServerError(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Internal server error."


@dataclass
class InvalidPasswordError(HTTPException):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail: str = "Wrong password"


@dataclass
class AuthenticationError(HTTPException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Unable to authenticate with provided credentials."


@dataclass
class UserAlreadyExistsError(HTTPException):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail: str = "Unavailable username"


@dataclass
class InvalidCredentialsError(HTTPException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Could not validate credentials"
    headers: dict = field(default_factory=lambda: {"WWW-Authenticate": "Bearer"})


@dataclass
class UserNotFoundError(HTTPException):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "User not found"


@dataclass
class InactiveUserError(HTTPException):
    status_code: int = status.HTTP_403_FORBIDDEN
    detail: str = "User is inactive"


@dataclass
class OperationNotPermittedError(HTTPException):
    status_code: int = status.HTTP_403_FORBIDDEN
    detail: str = "Operation not permitted"
