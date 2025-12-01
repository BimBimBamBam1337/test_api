from .base_errors import (
    RecordNotFoundError,
)


class SessionNotFoundError(RecordNotFoundError):
    __model__ = "Session"
