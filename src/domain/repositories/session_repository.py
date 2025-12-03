from abc import ABC, abstractmethod

from domain.models import SessionDomain
from infrastructure.utils.profiler import ProfileABCMeta


class AbstractSessionRepository(ABC, metaclass=ProfileABCMeta):

    @abstractmethod
    async def exists(self, id: int) -> bool:
        """
        Проверяет, существует ли сессия по ID.

        :param id: ID пользователя.
        :return: True, если пользователь существует, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        *,
        id: int,
        user_id: int,
        session_token: str,
        expires_at,
        ip: str | None = None,
        user_agent: str | None = None,
    ) -> SessionDomain:
        """
        Создаёт новую сессию.

        :param id: Уникальный идентификатор сессии.
        :param user_id: ID пользователя.
        :param session_token: Токен сессии.
        :param expires_at: Дата и время истечения сессии.
        :param ip: IP пользователя.
        :param user_agent: User-Agent браузера.
        :return: Доменная модель сессии.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> SessionDomain | None:
        """
        Возвращает сессию по ID, если найдена.

        :param id: ID сессии.
        :return: Доменная модель сессии или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_token(self, token: str) -> SessionDomain | None:
        """
        Возвращает сессию по токену.

        :param token: Токен сессии.
        :return: Доменная модель или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_user(self, user_id: int) -> list[SessionDomain]:
        """
        Возвращает все сессии пользователя.

        :param user_id: ID пользователя.
        :return: Список доменных моделей.
        """
        raise NotImplementedError

    @abstractmethod
    async def update_last_seen(self, id: int):
        """
        Обновляет поле последней активности.

        :param id: ID сессии.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> SessionDomain | None:
        """
        Удаляет сессию по ID.

        :param id: ID сессии.
        :return: True, если удалена, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_user_sessions(self, user_id: int) -> int:
        """
        Удаляет все сессии конкретного пользователя.

        :param user_id: ID пользователя.
        :return: Количество удалённых сессий.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_expired(self) -> int:
        """
        Удаляет все истекшие сессии.

        :return: Количество удалённых сессий.
        """
        raise NotImplementedError
