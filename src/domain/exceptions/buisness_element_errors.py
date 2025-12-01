from .base_errors import RecordNotFoundError, RecordAlreadyExistsError


class BuisnessElementAlreadyExistsError(RecordAlreadyExistsError):
    __model__ = "BuisnessElement"


class BuisnessElementNotFoundError(RecordNotFoundError):
    __model__ = "BuisnessElement"
