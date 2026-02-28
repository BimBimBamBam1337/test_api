from domain.exceptions import NotFoundError, AlreadyExistsError


class EmployeeNotFoundError(NotFoundError):
    pass


class EmployeeAlreadyExistsError(AlreadyExistsError):
    pass
