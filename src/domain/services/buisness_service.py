from domain.exceptions import (
    BuisnessElementAlreadyExistsError,
    BuisnessElementNotFoundError,
)
from domain.models import BuisnessElementDomain
from domain.uow import AbstractUnitOfWork


class BusinessElementService:
    def __init__(self, uow: AbstractUnitOfWork):

        self.__element_repo = uow.buisness_element_repo

    async def exists(self, id: int) -> bool:
        """
        Проверяет, существует ли объект бизнес-приложения с указанным ID.

        :param id: ID объекта.
        :return: True, если объект существует, иначе False.
        """
        return await self.__element_repo.exists(id)

    async def create_element(
        self, *, id: int, code: str, name: str
    ) -> BuisnessElementDomain:
        """
        Создаёт новый объект бизнес-приложения.

        :param id: Уникальный идентификатор объекта.
        :param name: Название объекта.
        :return: Доменная модель объекта.
        :raise BuisnessElementAlreadyExistsError: Если объект с таким названием уже существует.
        """
        existing = await self.__element_repo.get_by_name(name)
        if existing is not None:
            raise BuisnessElementNotFoundError(name=name)

        element = await self.__element_repo.create(id=id, code=code, name=name)
        return element

    async def get_element_by_id(self, id: int) -> BuisnessElementDomain:
        """
        Возвращает объект бизнес-приложения по его ID.

        :param id: ID объекта.
        :return: Доменная модель объекта.
        :raise BuisnessElementNotFoundError: Если объект не найден.
        """
        element = await self.__element_repo.get_by_id(id)
        if element is None:
            raise BuisnessElementNotFoundError(id=id)
        return element

    async def get_element_by_name(self, name: str) -> BuisnessElementDomain:
        """
        Возвращает объект бизнес-приложения по его названию.

        :param name: Название объекта.
        :return: Доменная модель объекта.
        :raise BuisnessElementNotFoundError: Если объект не найден.
        """
        element = await self.__element_repo.get_by_name(name)
        if element is None:
            raise BuisnessElementNotFoundError(name=name)
        return element

    async def update_element(self, id: int, *, name: str) -> BuisnessElementDomain:
        """
        Обновляет название объекта бизнес-приложения.

        :param id: ID объекта.
        :param name: Новое название объекта.
        :return: Обновлённая доменная модель объекта.
        :raise BuisnessElementAlreadyExistsError: Если объект с таким названием уже существует.
        :raise BuisnessElementNotFoundError: Если объект с указанным ID не найден.
        """
        existing = await self.__element_repo.get_by_name(name)
        if existing is not None and existing.id != id:
            raise BuisnessElementAlreadyExistsError(name=name)

        updated = await self.__element_repo.update(id, name=name)
        if updated is None:
            raise BuisnessElementNotFoundError(id=id)
        return updated

    async def delete_element(self, id: int) -> BuisnessElementDomain:
        """
        Удаляет объект бизнес-приложения по ID.

        :param id: ID объекта.
        :return: Удалённая доменная модель объекта.
        :raise BuisnessElementNotFoundError: Если объект не найден.
        """
        deleted = await self.__element_repo.delete(id)
        if deleted is None:
            raise BuisnessElementNotFoundError(id=id)
        return deleted

    async def list_elements(self) -> list[BuisnessElementDomain]:
        """
        Возвращает список всех объектов бизнес-приложения.

        :return: Список доменных моделей объектов.
        """
        return await self.__element_repo.get_all()
