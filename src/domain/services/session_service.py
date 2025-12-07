from datetime import datetime, timedelta
from uuid import UUID

from domain.exceptions import SessionNotFoundError
from domain.models import SessionDomain
from domain.uow import AbstractUnitOfWork


from datetime import datetime, timedelta

from domain.exceptions import SessionNotFoundError
from domain.models import SessionDomain
from domain.uow import AbstractUnitOfWork


class SessionService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.__session_repo = uow.session_repo

    async def exists(self, id: str) -> bool:
        """
        Проверяет, существует ли сессия с указанным ID.

        :param id: ID сессии.
        :return: True, если сессия существует, иначе False.
        """
        return await self.__session_repo.exists(id)

    async def create_session(
        self,
        *,
        id: UUID,
        user_id: int,
        session_token: str,
        expires_at: datetime | None = None,
        ip: str | None = None,
        user_agent: str | None = None,
    ) -> SessionDomain:
        """
        Создаёт новую сессию пользователя.

        :param id: Уникальный идентификатор сессии.
        :param user_id: ID пользователя.
        :param session_token: Токен сессии.
        :param expires_at: Дата и время истечения сессии. По умолчанию +1 день.
        :param ip: IP-адрес пользователя.
        :param user_agent: User-Agent браузера.
        :return: Доменная модель сессии.
        """
        if expires_at is None:
            expires_at = datetime.utcnow() + timedelta(days=1)

        session = await self.__session_repo.create(
            id=id,
            user_id=user_id,
            session_token=session_token,
            expires_at=expires_at,
            ip=ip,
            user_agent=user_agent,
        )
        return session

    async def get_session_by_id(self, id: str) -> SessionDomain:
        """
        Возвращает сессию по её уникальному ID.

        :param id: ID сессии.
        :return: Доменная модель сессии.
        :raise SessionNotFoundError: Если сессия не найдена.
        """
        session = await self.__session_repo.get_by_id(id)
        if session is None:
            raise SessionNotFoundError(id=id)
        return session

    async def get_session_by_token(self, token: str) -> SessionDomain:
        """
        Возвращает сессию по токену.

        :param token: Токен сессии.
        :return: Доменная модель сессии.
        :raise SessionNotFoundError: Если сессия не найдена.
        """
        session = await self.__session_repo.get_by_token(token)
        if session is None:
            raise SessionNotFoundError(token=token)
        return session

    async def get_user_sessions(self, user_id: int) -> list[SessionDomain]:
        """
        Возвращает список всех сессий пользователя.

        :param user_id: ID пользователя.
        :return: Список доменных моделей сессий.
        """
        return await self.__session_repo.get_by_user(user_id)

    async def update_last_seen(self, id: str):
        """
        Обновляет время последней активности сессии.

        :param id: ID сессии.
        """
        await self.__session_repo.update_last_seen(id)

    async def delete_session(self, id: str) -> SessionDomain:
        """
        Удаляет сессию по её ID.

        :param id: ID сессии.
        :return: True, если сессия была удалена.
        :raise SessionNotFoundError: Если сессия не найдена.
        """
        success = await self.__session_repo.delete(id)
        if not success:
            raise SessionNotFoundError(id=id)
        return success

    async def delete_user_sessions(self, user_id: int) -> int:
        """
        Удаляет все сессии конкретного пользователя.

        :param user_id: ID пользователя.
        :return: Количество удалённых сессий.
        """
        return await self.__session_repo.delete_user_sessions(user_id)

    async def delete_expired_sessions(self) -> int:
        """
        Удаляет все сессии, срок действия которых истёк.

        :return: Количество удалённых сессий.
        """
        return await self.__session_repo.delete_expired()
