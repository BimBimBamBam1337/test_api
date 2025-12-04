from fastapi import APIRouter, Body, Path, Depends
from domain.models import UserDomain
from presentation.api.dependencies import (
    get_access_role_rules_handler,
    get_user_from_verify_token,
)
from presentation.api.handlers import AccessRoleRulesHandler
from presentation.api.schemas import (
    AccessRoleRuleResponse,
    CreateAccessRoleRuleRequest,
    UpdateAccessRoleRuleRequest,
)

router = APIRouter(prefix="/access-role-rules", tags=["Access Role Rules"])


@router.get(
    "",
    summary="Список всех правил доступа ролей",
    response_model=list[AccessRoleRuleResponse],
)
async def list_access_role_rules_handler(
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: AccessRoleRulesHandler = Depends(get_access_role_rules_handler),
):
    return await handler.list_rules(user.role)


@router.post(
    "",
    summary="Создание нового правила доступа",
    response_model=AccessRoleRuleResponse,
)
async def create_access_role_rule_handler(
    rule_data: CreateAccessRoleRuleRequest = Body(...),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: AccessRoleRulesHandler = Depends(get_access_role_rules_handler),
):
    return await handler.create_rule(rule_data=rule_data, initiator=user.role)


@router.patch(
    "/{rule_id}",
    summary="Обновление правила доступа",
    response_model=AccessRoleRuleResponse,
)
async def update_access_role_rule_handler(
    rule_id: int = Path(..., description="ID правила доступа"),
    rule_data: UpdateAccessRoleRuleRequest = Body(...),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: AccessRoleRulesHandler = Depends(get_access_role_rules_handler),
):
    return await handler.update_rule(
        rule_id=rule_id, rule_data=rule_data, initiator=user.role
    )


@router.delete(
    "/{rule_id}",
    summary="Удаление правила доступа",
    response_model=AccessRoleRuleResponse,
)
async def delete_access_role_rule_handler(
    rule_id: int = Path(..., description="ID правила доступа"),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: AccessRoleRulesHandler = Depends(get_access_role_rules_handler),
):
    return await handler.delete_rule(rule_id=rule_id, initiator=user.role)
