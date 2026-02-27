from domain.exceptions import NotFoundError, AlreadyExistsError


class DepartamentNotFoundError(NotFoundError):
    pass


class DepartamentAlreadyExistsError(AlreadyExistsError):
    pass
