from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from skuf import Dependency

from config import settings
from domain.exceptions import NotPermissionError
from domain.models import UserDomain, Role
from domain.services import UserService
from domain.uow import AbstractUnitOfWork
from infrastructure.database.enigne import SessionFactory
from infrastructure.database.uow import UnitOfWork
from infrastructure.utils.jwt import decode_token
from infrastructure.utils.logger_config import log
from presentation.api.handlers import (
    UsersHandler,
    RoleHandler,
    AccessRoleRulesHandler,
    SessionHandler,
    RefreshTokenHandler,
    BuisnessElementHandler,
    AuthHandler,
)


async def get_uow() -> AsyncGenerator[UnitOfWork]:
    async with UnitOfWork(SessionFactory) as uow:
        log.debug("UnitOfWork started transaction")
        yield uow
        log.debug("UnitOfWork finished transaction")


async def get_auth_handler(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> AuthHandler:
    return AuthHandler(uow)


async def get_session_handler(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> SessionHandler:
    return SessionHandler(uow)


async def get_refresh_token_handler(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> RefreshTokenHandler:
    return RefreshTokenHandler(uow)


async def get_buisness_element_handler(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> BuisnessElementHandler:
    return BuisnessElementHandler(uow)


async def get_user_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> UserService:
    return UserService(uow)


async def get_roles_handler(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> RoleHandler:
    return RoleHandler(uow)


async def get_users_handler(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> UsersHandler:
    return UsersHandler(uow)


async def get_access_role_rules_handler(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> AccessRoleRulesHandler:
    return AccessRoleRulesHandler(uow)


def get_user_id_from_verify_token(
    bearer: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> int:
    payload = decode_token(bearer.credentials, settings.secret_key)
    user_id = payload.get("user_id")
    if user_id is None:
        raise JWTError("Invalid token type")
    return user_id


async def get_user_from_verify_token(
    user_id: int = Depends(get_user_id_from_verify_token),
    user_service: UserService = Depends(get_user_service),
) -> UserDomain:
    return await user_service.get_user_by_id(user_id)


async def get_admin_from_verify_token(
    user: UserDomain = Depends(get_user_from_verify_token),
) -> None:
    if user.role == Role.MANAGER:
        raise NotPermissionError()
