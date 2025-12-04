from domain.exceptions import NotPermissionError
from domain.models import UserDomain, Role
from domain.services import RefreshTokenService
from domain.uow import AbstractUnitOfWork
from infrastructure.utils.logger_config import log
from presentation.api.schemas import (
    RefreshTokenResponse,
    ListRefreshTokenResponse,
    CreateRefreshTokenResponse,
)


class RefreshTokenHandler:
    def __init__(self, uow: AbstractUnitOfWork):
        self.token_service = RefreshTokenService(uow)

    async def create_token(
        self, token_data: CreateRefreshTokenResponse, initiator: UserDomain
    ):
        # Только админ может создавать токен для любого пользователя
        if initiator.role != Role.ADMIN and initiator.id != token_data.user_id:
            raise NotPermissionError("Cannot create token for another user")

        token = await self.token_service.create_token(
            id=token_data.id,
            user_id=token_data.user_id,
            token_hash=token_data.token_hash,
            expires_at=token_data.expires_at,
        )
        log.info("Created refresh token: {}", token)
        return RefreshTokenResponse.from_domain(token)

    async def get_token(self, token_id: int, initiator: UserDomain):
        token = await self.token_service.get_token_by_id(token_id)
        if initiator.role != Role.ADMIN and initiator.id != token.user_id:
            raise NotPermissionError("Cannot view token of another user")
        return RefreshTokenResponse.from_domain(token)

    async def list_tokens(self, initiator: UserDomain):
        tokens = await self.token_service.list_tokens()
        if initiator.role != Role.ADMIN:
            # Пользователь видит только свои токены
            tokens = [t for t in tokens if t.user_id == initiator.id]
        return ListRefreshTokenResponse.from_domain(tokens)

    async def revoke_token(self, token_id: int, initiator: UserDomain):
        token = await self.token_service.get_token_by_id(token_id)
        if initiator.role != Role.ADMIN and initiator.id != token.user_id:
            raise NotPermissionError("Cannot revoke token of another user")

        revoked = await self.token_service.revoke_token(token_id)
        log.info("Revoked refresh token: {}", revoked)
        return RefreshTokenResponse.from_domain(revoked)

    async def revoke_user_tokens(self, user_id: int, initiator: UserDomain):
        if initiator.role != Role.ADMIN and initiator.id != user_id:
            raise NotPermissionError("Cannot revoke tokens of another user")

        count = await self.token_service.revoke_user_tokens(user_id)
        log.info("Revoked {} tokens for user {}", count, user_id)
        return {"revoked_count": count}
