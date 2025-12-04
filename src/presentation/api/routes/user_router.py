from fastapi import APIRouter, Body, Depends, Path, status

from domain.models import UserDomain
from presentation.api.v2.dependencies import (
    get_user_from_verify_token,
    get_users_handler,
)
from presentation.api.handlers import UsersHandler
from presentation.api.schemas import (
    CreateUserRequest,
    ListUsersResponse,
    UpdateUserRequest,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["User"])


@router.get(
    "/me",
    summary="Получение информации о текущем пользователе",
    response_description="Возвращает информацию о пользователе.",
    response_model=UserResponse,
)
async def users_me_handler(
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: UsersHandler = Depends(get_users_handler),
):
    return await handler.me(user)


@router.get(
    "",
    summary="Получение списка пользователей",
    description="**Для администратора** - вернет всех пользователей кроме админитсраторов.\n"
    "**Для ропов** - вернет всех менеджеров и окк, у которых он присвоен.\n",
    response_description="Возвращает список менеджеров",
    response_model=ListUsersResponse,
)
async def users__handler(
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: UsersHandler = Depends(get_users_handler),
):
    return await handler.get_users(initiator=user)


@router.post(
    "",
    summary="Создание пользователя",
    description="Создает нового пользователя в системе. Доступно для администраторов",
    response_description="Возвращает информацию о созданном пользователе",
    response_model=UserResponse,
)
async def user_create_handler(
    user_data: CreateUserRequest = Body(...),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: UsersHandler = Depends(get_users_handler),
):
    return await handler.create_user(
        user_data=user_data,
        initiator=user,
    )


@router.patch(
    "/{user_id}",
    summary="Обновление пользователя",
    response_description="Возвращает информацию об обновленном пользователе",
    response_model=UserResponse,
)
async def user_update_handler(
    user_id: int = Path(..., description="Идентификатор пользователя"),
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
    summary="Удаление пользователя",
    description="Удаляет пользователя из системы",
    response_description="Возвращает информацию об удаленном пользователе",
    response_model=UserResponse,
)
async def user_delete_handler(
    user_id: int = Path(..., description="Идентификатор пользователя"),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: UsersHandler = Depends(get_users_handler),
):
    return await handler.delete_user(user_id=user_id, initiator=user)
