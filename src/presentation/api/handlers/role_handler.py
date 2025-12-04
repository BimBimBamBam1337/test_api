from domain.exceptions import NotPermissionError
from domain.models import UserDomain
from domain.services import RoleService
from domain.uow import AbstractUnitOfWork
from infrastructure.utils.logger_config import log
from presentation.api.schemas import (
    RoleResponse,
    ListRoleResponse,
    CreateRoleRequest,
    UpdateRoleRequest,
)


class RoleHandler:
    def __init__(self, uow: AbstractUnitOfWork):
        self.role_service = RoleService(uow)

    async def create_role(
        self, role_data: CreateRoleRequest, initiator: UserDomain
    ) -> RoleResponse:
        if initiator.role != "ADMIN":
            raise NotPermissionError("Only ADMIN can create roles")

        role = await self.role_service.create_role(
            id=role_data.id,
            role_name=role_data.role,
        )
        log.info("Created Role: {}", role)
        return RoleResponse.from_domain(role)

    async def get_role(self, role_id: int) -> RoleResponse:
        role = await self.role_service.get_role_by_id(role_id)
        return RoleResponse.from_domain(role)

    async def list_roles(self) -> ListRoleResponse:
        roles = await self.role_service.list_roles()
        return ListRoleResponse.from_domain(roles)

    async def update_role(
        self, role_id: int, role_data: UpdateRoleRequest, initiator: UserDomain
    ) -> RoleResponse | None:
        if initiator.role != "ADMIN":
            raise NotPermissionError("Only ADMIN can update roles")

        role = await self.role_service.update_role(role_id, role=role_data.role)
        log.info("Updated Role: {}", role)
        return RoleResponse.from_domain(role)

    async def delete_role(self, role_id: int, initiator: UserDomain) -> RoleResponse:
        if initiator.role != "ADMIN":
            raise NotPermissionError("Only ADMIN can delete roles")

        role = await self.role_service.delete_role(role_id)
        log.info("Deleted Role: {}", role)
        return RoleResponse.from_domain(role)
