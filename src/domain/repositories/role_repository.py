from abc import ABC, abstractmethod

from domain.models import RoleDomain
from infrastructure.utils.profiler import ProfileABCMeta


class AbstractRoleRepository(ABC, metaclass=ProfileABCMeta):
    @abstractmethod
    async def exists(self, id: int) -> bool:
        """
        Проверяет, существует ли роль по ID.

        :param id: ID пользователя.
        :return: True, если пользователь существует, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(
        self, *, id: int, name: str, description: str | None = None
    ) -> RoleDomain:
        """
        Создаёт новую роль.

        :param id: Уникальный идентификатор роли.
        :param name: Название роли (например, 'admin', 'user').
        :param description: Описание роли.
        :return: Доменная модель роли.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> RoleDomain | None:
        """
        Возвращает роль по ID, если найдена.

        :param id: ID роли.
        :return: Доменная модель роли или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> RoleDomain | None:
        """
        Возвращает роль по имени.

        :param name: Название роли.
        :return: Доменная модель роли или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, id: int, *, name: str | None = None, description: str | None = None
    ) -> RoleDomain | None:
        """
        Обновляет данные роли.

        :param id: ID роли.
        :param name: Новое название роли.
        :param description: Новое описание роли.
        :return: Обновлённая доменная модель роли или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> RoleDomain | None:
        """
        Удаляет роль по ID.

        :param id: ID роли.
        :return: True, если роль удалена, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[RoleDomain]:
        """
        Возвращает все роли.

        :return: Список доменных моделей ролей.
        """
        raise NotImplementedError
