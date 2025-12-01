from .base_errors import RecordNotFoundError, RecordAlreadyExistsError


class RoleAlreadyExistsError(RecordAlreadyExistsError):
    __model__ = "Role"


class RoleNotFoundError(RecordNotFoundError):
    __model__ = "Role"
