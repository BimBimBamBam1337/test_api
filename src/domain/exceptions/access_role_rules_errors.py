from .base_errors import RecordNotFoundError, RecordAlreadyExistsError


class AccessRoleRuleAlreadyExistsError(RecordAlreadyExistsError):
    __model__ = "AccessRoleRules"


class AccessRoleRuleNotFoundError(RecordNotFoundError):
    __model__ = "AccessRoleRules"
