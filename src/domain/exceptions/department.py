from domain.exceptions import NotFoundError, AlreadyExistsError


class DepartmentNotFoundError(NotFoundError):
    pass


class DepartmentAlreadyExistsError(AlreadyExistsError):
    pass
