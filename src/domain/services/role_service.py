from domain.exceptions import RoleAlreadyExistsError, RoleNotFoundError
from domain.models import RoleDomain
from domain.uow import AbstractUnitOfWork


class RoleService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.__role_repo = uow.role_repo

    async def exists(self, id: int) -> bool:
        """
        Проверяет, существует ли роль с указанным ID.

        :param id: ID роли.
        :return: True, если роль существует, иначе False.
        """
        return await self.__role_repo.exists(id)

    async def create_role(self, *, id: int, name: str) -> RoleDomain:
        """
        Создаёт новую роль.

        :param id: Уникальный идентификатор роли.
        :param name: Название роли.
        :return: Доменная модель роли.
        :raise RoleAlreadyExistsError: Если роль с таким названием уже существует.
        """
        existing = await self.__role_repo.get_by_name(name)
        if existing is not None:
            raise RoleAlreadyExistsError(name=name)

        role = await self.__role_repo.create(id=id, name=name)
        return role

    async def get_role_by_id(self, id: int) -> RoleDomain:
        """
        Возвращает роль по её ID.

        :param id: ID роли.
        :return: Доменная модель роли.
        :raise RoleNotFoundError: Если роль не найдена.
        """
        role = await self.__role_repo.get_by_id(id)
        if role is None:
            raise RoleNotFoundError(id=id)
        return role

    async def get_role_by_name(self, name: str) -> RoleDomain:
        """
        Возвращает роль по её названию.

        :param name: Название роли.
        :return: Доменная модель роли.
        :raise RoleNotFoundError: Если роль не найдена.
        """
        role = await self.__role_repo.get_by_name(name)
        if role is None:
            raise RoleNotFoundError(name=name)
        return role

    async def update_role(self, id: int, *, name: str) -> RoleDomain:
        """
        Обновляет название роли.

        :param id: ID роли.
        :param name: Новое название роли.
        :return: Обновлённая доменная модель роли.
        :raise RoleAlreadyExistsError: Если новая роль с таким названием уже существует.
        :raise RoleNotFoundError: Если роль с указанным ID не найдена.
        """
        existing = await self.__role_repo.get_by_name(name)
        if existing is not None and existing.id != id:
            raise RoleAlreadyExistsError(name=name)

        updated = await self.__role_repo.update(id, name=name)
        if updated is None:
            raise RoleNotFoundError(id=id)
        return updated

    async def delete_role(self, id: int) -> RoleDomain:
        """
        Удаляет роль по ID.

        :param id: ID роли.
        :return: Удалённая доменная модель роли.
        :raise RoleNotFoundError: Если роль не найдена.
        """
        deleted = await self.__role_repo.delete(id)
        if deleted is None:
            raise RoleNotFoundError(id=id)
        return deleted

    async def list_roles(self) -> list[RoleDomain]:
        """
        Возвращает список всех ролей.

        :return: Список доменных моделей ролей.
        """
        return await self.__role_repo.get_all()
