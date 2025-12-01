from .base_errors import (
    RecordNotFoundError,
    RecordAlreadyExistsError,
)


class RefreshTokenNotFoundError(RecordNotFoundError):
    __model__ = "RefreshToken"


class RefreshTokenAlreadyExistsError(RecordAlreadyExistsError):
    __model__ = "RefreshToken"
