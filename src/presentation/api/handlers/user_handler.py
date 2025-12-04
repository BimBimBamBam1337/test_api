from domain.exceptions import NotPermissionError
from domain.models import UserDomain, Role
from domain.services import UserService
from domain.uow import AbstractUnitOfWork
from infrastructure.utils.logger_config import log
from presentation.api.schemas import (
    UserResponse,
    ListUsersResponse,
    CreateUserRequest,
    UpdateUserRequest,
)


class UsersHandler:
    def __init__(self, uow: AbstractUnitOfWork):
        self.user_service = UserService(uow)

    async def me(self, user: UserDomain) -> UserResponse:
        """Получение информации о текущем пользователе"""
        return UserResponse.from_domain(user)

    async def list_users(self, initiator: UserDomain) -> ListUsersResponse:
        """Список пользователей (для ADMIN и MANAGER)"""
        if initiator.role not in [Role.ADMIN, Role.MANAGER]:
            raise NotPermissionError("Access denied")

        users = await self.user_service.list_users()
        # MANAGER не видит ADMIN-ов
        if initiator.role == Role.MANAGER:
            users = [u for u in users if u.role != Role.ADMIN]

        return ListUsersResponse.from_domain(users)

    async def create_user(
        self, user_data: CreateUserRequest, initiator: UserDomain
    ) -> UserResponse:
        """Создание нового пользователя"""
        if initiator.role != Role.ADMIN:
            raise NotPermissionError("Only ADMIN can create users")

        # ADMIN не может создавать других ADMIN-ов
        if user_data.role == Role.ADMIN:
            raise NotPermissionError("Cannot create ADMIN users")

        user = await self.user_service.create_user(
            id=user_data.id,
            name=user_data.name,
            username=user_data.username,
            password=user_data.password,
            role=user_data.role,
            check_valid_fields=True,
        )

        log.info("Created User: {}", user)
        return UserResponse.from_domain(user)

    async def update_user(
        self, user_id: int, user_data: UpdateUserRequest, initiator: UserDomain
    ) -> UserResponse:
        """Обновление пользователя"""
        target_user = await self.user_service.get_user_by_id(user_id)

        # ADMIN нельзя обновлять через API
        if target_user.role == Role.ADMIN:
            raise NotPermissionError("Cannot update ADMIN users")

        # MANAGER может обновлять только пользователей, кроме ADMIN
        if initiator.role not in [Role.ADMIN, Role.MANAGER]:
            raise NotPermissionError("Access denied")

        updated_user = await self.user_service.update_user(
            user_id=user_id,
            name=user_data.name,
            username=user_data.username,
            password=user_data.password,
            role=user_data.role,
        )

        log.info("Updated User: {}", updated_user)
        return UserResponse.from_domain(updated_user)

    async def delete_user(self, user_id: int, initiator: UserDomain) -> UserResponse:
        """Мягкое удаление пользователя (is_active=False)"""
        target_user = await self.user_service.get_user_by_id(user_id)

        # ADMIN нельзя удалять через API
        if target_user.role == Role.ADMIN:
            raise NotPermissionError("Cannot delete ADMIN users")

        if initiator.role not in [Role.ADMIN, Role.MANAGER]:
            raise NotPermissionError("Access denied")

        deleted_user = await self.user_service.delete_user(user_id)

        log.info("Deleted User: {}", deleted_user)
        return UserResponse.from_domain(deleted_user)
