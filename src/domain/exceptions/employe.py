from domain.exceptions import NotFoundError, AlreadyExistsError


class EmployeNotFoundError(NotFoundError):
    pass


class EmployeAlreadyExistsError(AlreadyExistsError):
    pass
