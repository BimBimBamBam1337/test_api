from fastapi import APIRouter, Body, Depends, Request, status

from domain.models import UserDomain
from presentation.api.dependencies import (
    get_auth_handler,
    get_user_from_verify_token,
)
from presentation.api.handlers import AuthHandler
from presentation.api.schemas import (
    AuthLoginRequest,
    AuthLoginResponse,
    AuthRefreshResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    summary="Аутентификация",
    description="Выполняет вход в систему по логину и паролю, возвращает токены доступа",
    response_model=AuthLoginResponse,
)
async def auth_login_handler(
    request: Request,
    body: AuthLoginRequest = Body(),
    handler: AuthHandler = Depends(get_auth_handler),
):
    return await handler.login(body)


@router.post(
    "/logout",
    summary="Выход из аккаунта",
    description="Выполняет выход из системы и инвалидирует токены текущего пользователя",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def auth_logout_handler(
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: AuthHandler = Depends(get_auth_handler),
):
    return await handler.logout(user)


@router.post(
    "/refresh",
    summary="Обновление токена",
    description="Обновляет токен доступа с помощью refresh токена из cookies",
    response_model=AuthRefreshResponse,
)
async def auth_refresh_handler(
    request: Request,
    handler: AuthHandler = Depends(get_auth_handler),
):
    refresh_token = request.cookies.get("refresh_token")
    return await handler.refresh(refresh_token)


@router.get(
    "/status",
    summary="Проверка токена",
    description="Проверяет валидность текущего токена доступа пользователя",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def auth_status_handler(
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: AuthHandler = Depends(get_auth_handler),
):
    return await handler.status(user)
