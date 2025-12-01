from datetime import datetime, timedelta


from domain.exceptions import RefreshTokenNotFoundError
from domain.models import RefreshTokenDomain
from domain.uow import AbstractUnitOfWork


class RefreshTokenService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.__token_repo = uow.refresh_token_repo

    async def exists(self, id: int) -> bool:
        """
        Проверяет, существует ли refresh-токен с указанным ID.

        :param id: ID токена.
        :return: True, если токен существует, иначе False.
        """
        return await self.__token_repo.exists(id)

    async def create_token(
        self,
        *,
        id: int,
        user_id: int,
        token_hash: str,
        expires_at: datetime | None = None,
    ) -> RefreshTokenDomain:
        """
        Создаёт новый refresh-токен для пользователя.

        :param id: Уникальный идентификатор токена.
        :param user_id: ID пользователя.
        :param token_hash: Хэш refresh-токена.
        :param expires_at: Время истечения токена. По умолчанию +30 дней.
        :return: Доменная модель refresh-токена.
        """
        if expires_at is None:
            expires_at = datetime.utcnow() + timedelta(days=30)

        token = await self.__token_repo.create(
            id=id, user_id=user_id, token_hash=token_hash, expires_at=expires_at
        )
        return token

    async def get_token_by_id(self, id: int) -> RefreshTokenDomain:
        """
        Возвращает refresh-токен по ID.

        :param id: ID токена.
        :return: Доменная модель refresh-токена.
        :raise RefreshTokenNotFoundError: Если токен не найден.
        """
        token = await self.__token_repo.get_by_id(id)
        if token is None:
            raise RefreshTokenNotFoundError(id=id)
        return token

    async def get_user_tokens(self, user_id: int) -> list[RefreshTokenDomain]:
        """
        Возвращает все refresh-токены пользователя.

        :param user_id: ID пользователя.
        :return: Список доменных моделей токенов.
        """
        return await self.__token_repo.get_by_user(user_id)

    async def revoke_token(self, id: int) -> RefreshTokenDomain | None:
        """
        Отзывает конкретный refresh-токен по ID.

        :param id: ID токена.
        :return: Отозванная доменная модель токена.
        :raise RefreshTokenNotFoundError: Если токен не найден.
        """
        revoked = await self.__token_repo.revoke(id)
        if not revoked:
            raise RefreshTokenNotFoundError(id=id)
        token = await self.__token_repo.get_by_id(id)
        return token

    async def revoke_user_tokens(self, user_id: int) -> int:
        """
        Отзывает все refresh-токены конкретного пользователя.

        :param user_id: ID пользователя.
        :return: Количество отозванных токенов.
        """
        return await self.__token_repo.revoke_user_tokens(user_id)

    async def delete_expired_tokens(self) -> int:
        """
        Удаляет все истекшие refresh-токены.

        :return: Количество удалённых токенов.
        """
        return await self.__token_repo.delete_expired()

    async def list_tokens(self) -> list[RefreshTokenDomain]:
        """
        Возвращает все refresh-токены.

        :return: Список доменных моделей токенов.
        """
        return await self.__token_repo.get_all()
