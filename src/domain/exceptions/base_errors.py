from typing import Any


class BaseRecordError(Exception):
    def __init__(self, model: str, fields: dict[str, Any], message: str):
        self.model = model
        self.fields = fields
        self.base_message = message
        full_message = f"{model} with {self._format_fields(fields)} {message}"
        super().__init__(full_message)

    @staticmethod
    def _format_fields(fields: dict[str, Any]) -> str:
        return ", ".join(f"{key}={str(value)!r}" for key, value in fields.items())


class RecordAlreadyExistsError(BaseRecordError):
    __model__ = "Record"

    def __init__(self, **fields: Any):
        super().__init__(self.__model__, fields, "already exists.")


class RecordNotFoundError(BaseRecordError):
    __model__ = "Record"

    def __init__(self, **fields: Any):
        super().__init__(self.__model__, fields, "not found.")


class NotPermissionError(Exception):
    def __init__(self, message: str = "Not permission."):
        super().__init__(message)
