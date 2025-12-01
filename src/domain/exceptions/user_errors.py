from .base_errors import (
    RecordAlreadyExistsError,
    RecordNotFoundError,
)


class UserAlreadyExistsError(RecordAlreadyExistsError):
    __model__ = "User"


class UserNotFoundError(RecordNotFoundError):
    __model__ = "User"


class UserValidationError(Exception):
    __model__ = "User"


class UserInvalidPasswordError(Exception):
    __model__ = "User"

    def __init__(self):
        super().__init__("Invalid password")
