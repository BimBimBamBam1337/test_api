from abc import ABC, abstractmethod

from domain.models import UserDomain, Role
from infrastructure.utils.profiler import ProfileABCMeta


class AbstractUserRepository(ABC, metaclass=ProfileABCMeta):
    @abstractmethod
    async def exists(self, id: int) -> bool:
        """
        Проверяет, существует ли пользователь по ID.

        :param id: ID пользователя.
        :return: True, если пользователь существует, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        *,
        id: int,
        username: str,
        password: str,
        role: Role,
        name: str,
    ):
        """
        Создает нового пользователя и возвращает доменную модель пользователя.

        :param id: Идентификатор пользователя.
        :param username: Username пользователя.
        :param password: Нехешированный пароль пользователя.
        :param role: Роль пользователя.
        :param name: Имя пользователя.
        :return: Доменная модель пользователя.
        """

        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> UserDomain | None:
        """
        Возвращает пользователя по ID, если найден.

        :param id: ID пользователя.
        :return: Доменная модель пользователя или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> UserDomain | None:
        """
        Возвращает пользователя по имени, если найден.

        :param name: Имя пользователя.
        :return: Доменная модель пользователя или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> UserDomain | None:
        """
        Возвращает пользователя по username, если найден.

        :param username: Username пользователя.
        :return: Доменная модель пользователя или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        id: int,
        *,
        name: str | None = None,
        username: str | None = None,
        password: str | None = None,
        role: Role | None = None,
    ) -> UserDomain | None:
        """
        Обновляет данные пользователя. Возвращает обновлённую модель, если пользователь найден.

        :param id: ID пользователя.
        :param name: Имя пользователя.
        :param username: Username пользователя.
        :param password: Нехешированный пароль пользователя.
        :param role: Роль пользователя.
        :return: Обновлённая модель пользователя или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> UserDomain | None:
        """
        Удаляет пользователя по ID. Возвращает True, если пользователь был удалён.

        :param id: ID пользователя.
        :return: True, если пользователь был удалён, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, by_role: Role | None = None) -> list[UserDomain]:
        """
        Возвращает всех пользователей, с возможностью фильтрации по роли.

        :param by_role: Роль пользователя.
        :return: Список доменных моделей пользователей.
        """
        raise NotImplementedError

    @abstractmethod
    async def soft_delete(self, id: int) -> UserDomain | None:
        """
        Деактивирует пользователя (мягкое удаление).

        :param id: ID пользователя.
        :return: True, если пользователь был удалён, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    async def restore(self, id: int) -> UserDomain | None:
        """
        Восстанавливает пользователя после soft-delete.

        :param id: ID пользователя.
        :return: True, если пользователь был удалён, иначе False.
        """
        raise NotImplementedError
