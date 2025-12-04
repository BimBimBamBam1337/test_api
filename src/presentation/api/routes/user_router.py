from fastapi import APIRouter, Body, Depends, Path

from domain.models import UserDomain, Role
from presentation.api.dependencies import (
    get_user_from_verify_token,
    get_users_handler,
    get_auth_handler,
)
from presentation.api.handlers import UsersHandler, AuthHandler
from presentation.api.schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
    ListUsersResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    summary="Получение информации о текущем пользователе",
    response_model=UserResponse,
)
async def me_handler(
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: UsersHandler = Depends(get_users_handler),
):
    return await handler.me(user)


@router.patch(
    "/me",
    summary="Обновление информации текущего пользователя",
    response_model=UserResponse,
)
async def update_me_handler(
    user_data: UpdateUserRequest = Body(...),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: UsersHandler = Depends(get_users_handler),
):
    return await handler.update_user(
        user_id=user.id, user_data=user_data, initiator=user
    )


@router.delete(
    "/me",
    summary="Удаление собственного аккаунта",
    description="Мягкое удаление. Статус пользователя становится is_active=False, выполняется logout.",
    response_model=UserResponse,
)
async def delete_me_handler(
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: UsersHandler = Depends(get_users_handler),
    auth: AuthHandler = Depends(get_auth_handler),
):
    deleted = await handler.delete_user(user.id, initiator=user)
    await auth.logout(user)
    return deleted


@router.get(
    "",
    summary="Получение списка пользователей (только admin)",
    response_model=ListUsersResponse,
)
async def list_users_handler(
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: UsersHandler = Depends(get_users_handler),
):
    return await handler.get_users(initiator=user)


@router.patch(
    "/{user_id}",
    summary="Обновление пользователя (только admin)",
    response_model=UserResponse,
)
async def admin_update_user_handler(
    user_id: int = Path(...),
    user_data: UpdateUserRequest = Body(...),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: UsersHandler = Depends(get_users_handler),
):
    return await handler.update_user(
        user_id=user_id,
        user_data=user_data,
        initiator=user,
    )


@router.delete(
    "/{user_id}",
    summary="Удаление пользователя (только admin)",
    response_model=UserResponse,
)
async def admin_delete_user_handler(
    user_id: int = Path(...),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: UsersHandler = Depends(get_users_handler),
):
    return await handler.delete_user(user_id=user_id, initiator=user)
