from fastapi import APIRouter, Depends, Path, Body

from domain.models import UserDomain
from presentation.api.dependencies import (
    get_user_from_verify_token,
    get_roles_handler,
)
from presentation.api.handlers import RoleHandler
from presentation.api.schemas import (
    RoleResponse,
    ListRoleResponse,
    CreateRoleRequest,
    UpdateRoleRequest,
)

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get(
    "",
    summary="Получение списка ролей",
    description="Доступно только для администратора.",
    response_model=ListRoleResponse,
)
async def roles_list_handler(
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: RoleHandler = Depends(get_roles_handler),
):
    return await handler.list_roles()


@router.post(
    "",
    summary="Создание новой роли",
    description="Создает новую роль в системе. Доступно только для администратора.",
    response_model=RoleResponse,
)
async def role_create_handler(
    role_data: CreateRoleRequest = Body(...),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: RoleHandler = Depends(get_roles_handler),
):
    return await handler.create_role(role_data=role_data, initiator=user)


@router.patch(
    "/{role_id}",
    summary="Обновление роли",
    response_model=RoleResponse,
)
async def role_update_handler(
    role_id: int = Path(..., description="Идентификатор роли"),
    role_data: UpdateRoleRequest = Body(...),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: RoleHandler = Depends(get_roles_handler),
):
    return await handler.update_role(
        role_id=role_id,
        role_data=role_data,
        initiator=user,
    )


@router.delete(
    "/{role_id}",
    summary="Удаление роли",
    response_model=RoleResponse,
)
async def role_delete_handler(
    role_id: int = Path(..., description="Идентификатор роли"),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: RoleHandler = Depends(get_roles_handler),
):
    return await handler.delete_role(role_id=role_id, initiator=user)
