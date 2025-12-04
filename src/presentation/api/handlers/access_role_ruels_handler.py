from domain.exceptions import NotPermissionError
from domain.models import Role
from domain.services import AccessRoleRuleService
from domain.uow import AbstractUnitOfWork
from infrastructure.utils.logger_config import log
from presentation.api.schemas import (
    AccessRoleRuleResponse,
    CreateAccessRoleRuleRequest,
    UpdateAccessRoleRuleRequest,
)


class AccessRoleRulesHandler:
    def __init__(self, uow: AbstractUnitOfWork):
        self.access_role_rule_service = AccessRoleRuleService(uow)

    async def get_rule(self, rule_id: int, initiator: Role) -> AccessRoleRuleResponse:
        if initiator not in [Role.ADMIN, Role.MANAGER]:
            raise NotPermissionError("Access denied")

        rule = await self.access_role_rule_service.get_rule_by_id(rule_id)
        return AccessRoleRuleResponse.from_domain(rule)

    async def list_rules(self, initiator: Role) -> list[AccessRoleRuleResponse]:
        if initiator not in [Role.ADMIN, Role.MANAGER]:
            raise NotPermissionError("Access denied")

        rules = await self.access_role_rule_service.list_rules()
        return [AccessRoleRuleResponse.from_domain(rule) for rule in rules]

    async def create_rule(
        self, rule_data: CreateAccessRoleRuleRequest, initiator: Role
    ) -> AccessRoleRuleResponse:
        if initiator != Role.ADMIN:
            raise NotPermissionError("Only ADMIN can create rules")

        rule = await self.access_role_rule_service.create_rule(
            id=rule_data.id,
            role=rule_data.role,
            element_id=rule_data.element_id,
            read_permission=rule_data.read_permission,
            read_all_permission=rule_data.read_all_permission,
            create_permission=rule_data.create_permission,
            update_permission=rule_data.update_permission,
            update_all_permission=rule_data.update_all_permission,
            delete_permission=rule_data.delete_permission,
            delete_all_permission=rule_data.delete_all_permission,
        )

        log.info("Created AccessRoleRule: {}", rule)
        return AccessRoleRuleResponse.from_domain(rule)

    async def update_rule(
        self, rule_id: int, rule_data: UpdateAccessRoleRuleRequest, initiator: Role
    ) -> AccessRoleRuleResponse:
        if initiator != Role.ADMIN:
            raise NotPermissionError("Only ADMIN can update rules")

        rule = await self.access_role_rule_service.update_rule(
            id=rule_id,
            read_permission=rule_data.read_permission,
            read_all_permission=rule_data.read_all_permission,
            create_permission=rule_data.create_permission,
            update_permission=rule_data.update_permission,
            update_all_permission=rule_data.update_all_permission,
            delete_permission=rule_data.delete_permission,
            delete_all_permission=rule_data.delete_all_permission,
        )

        log.info("Updated AccessRoleRule: {}", rule)
        return AccessRoleRuleResponse.from_domain(rule)

    async def delete_rule(
        self, rule_id: int, initiator: Role
    ) -> AccessRoleRuleResponse:
        if initiator != Role.ADMIN:
            raise NotPermissionError("Only ADMIN can delete rules")

        deleted_rule = await self.access_role_rule_service.delete_rule(rule_id)
        log.info("Deleted AccessRoleRule: {}", deleted_rule)
        return AccessRoleRuleResponse.from_domain(deleted_rule)
