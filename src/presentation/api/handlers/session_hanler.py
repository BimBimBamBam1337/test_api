from datetime import datetime
from domain.exceptions import NotPermissionError
from domain.models import UserDomain, SessionDomain
from domain.services import SessionService
from domain.uow import AbstractUnitOfWork
from infrastructure.utils.logger_config import log
from presentation.api.schemas import SessionResponse, CreateSessionRequest


class SessionHandler:
    def __init__(self, uow: AbstractUnitOfWork):
        self.session_service = SessionService(uow)

    async def create_session(
        self,
        *,
        session_data: CreateSessionRequest,
        initiator: UserDomain,
    ) -> SessionResponse:
        """Создание новой сессии для пользователя"""
        session = await self.session_service.create_session(
            id=session_data.id,
            user_id=initiator.id,
            session_token=session_data.session_token,
            expires_at=session_data.expires_at,
            ip=session_data.ip,
            user_agent=session_data.user_agent,
        )
        log.info("Created Session: {}", session)
        return SessionResponse.from_domain(session)

    async def get_session(
        self, session_id: str, requester: UserDomain
    ) -> SessionResponse:
        """Получение сессии по ID"""
        session = await self.session_service.get_session_by_id(session_id)
        # Проверка, что пользователь может видеть только свои сессии
        if session.user_id != requester.id and requester.role != "ADMIN":
            raise NotPermissionError("Access denied to this session")
        return SessionResponse.from_domain(session)

    async def get_session_by_token(self, token: str) -> SessionResponse:
        """Получение сессии по токену (для аутентификации)"""
        session = await self.session_service.get_session_by_token(token)
        return SessionResponse.from_domain(session)

    async def list_user_sessions(
        self, user_id: int, requester: UserDomain
    ) -> list[SessionResponse]:
        """Список всех сессий пользователя"""
        if user_id != requester.id and requester.role != "ADMIN":
            raise NotPermissionError("Cannot view other user's sessions")

        sessions = await self.session_service.get_user_sessions(user_id)
        return [SessionResponse.from_domain(s) for s in sessions]

    async def update_last_seen(self, session_id: str):
        await self.session_service.update_last_seen(session_id)

    async def delete_session(
        self, session_id: str, requester: UserDomain
    ) -> SessionDomain:
        session = await self.session_service.get_session_by_id(session_id)
        if session.user_id != requester.id and requester.role != "ADMIN":
            raise NotPermissionError("Cannot delete other user's session")
        success = await self.session_service.delete_session(session_id)
        log.info("Deleted Session: {}", session_id)
        return success

    async def delete_user_sessions(self, user_id: int, requester: UserDomain) -> int:
        if user_id != requester.id and requester.role != "ADMIN":
            raise NotPermissionError("Cannot delete other user's sessions")
        count = await self.session_service.delete_user_sessions(user_id)
        log.info("Deleted {} sessions for user {}", count, user_id)
        return count

    async def delete_expired_sessions(self) -> int:
        count = await self.session_service.delete_expired_sessions()
        log.info("Deleted {} expired sessions", count)
        return count
