from abc import ABC, abstractmethod

from domain.models import RefreshTokenDomain
from infrastructure.utils.profiler import ProfileABCMeta


class AbstractRefreshTokenRepository(ABC, metaclass=ProfileABCMeta):
    @abstractmethod
    async def create(
        self,
        *,
        id: int,
        user_id: int,
        token_hash: str,
        expires_at,
    ) -> RefreshTokenDomain:
        """
        Создаёт новый refresh-токен.

        :param id: Уникальный идентификатор токена.
        :param user_id: ID пользователя.
        :param token_hash: Хэш refresh-токена.
        :param expires_at: Дата и время истечения токена.
        :return: Доменная модель refresh-токена.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> RefreshTokenDomain | None:
        """
        Возвращает refresh-токен по ID, если найден.

        :param id: ID токена.
        :return: Доменная модель токена или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_user(self, user_id: int) -> list[RefreshTokenDomain]:
        """
        Возвращает все refresh-токены конкретного пользователя.

        :param user_id: ID пользователя.
        :return: Список доменных моделей токенов.
        """
        raise NotImplementedError

    @abstractmethod
    async def revoke(self, id: int) -> bool:
        """
        Отзывает конкретный refresh-токен.

        :param id: ID токена.
        :return: True, если токен был успешно отозван, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    async def revoke_user_tokens(self, user_id: int) -> int:
        """
        Отзывает все refresh-токены конкретного пользователя.

        :param user_id: ID пользователя.
        :return: Количество отозванных токенов.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_expired(self) -> int:
        """
        Удаляет все истекшие refresh-токены.

        :return: Количество удалённых токенов.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[RefreshTokenDomain]:
        """
        Возвращает все refresh-токены.

        :return: Список доменных моделей токенов.
        """
        raise NotImplementedError
