from abc import ABC, abstractmethod

from domain.models import BuisnessElementDomain
from infrastructure.utils.profiler import ProfileABCMeta


class AbstractBusinessElementRepository(ABC, metaclass=ProfileABCMeta):
    @abstractmethod
    async def exists(self, id: int) -> bool:
        """
        Проверяет, существует ли элемент бизнеса по ID.

        :param id: ID пользователя.
        :return: True, если пользователь существует, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(
        self, *, id: int, code: str, name: str, commit: str | None = None
    ) -> BuisnessElementDomain:
        """
        Создаёт новый бизнес-элемент.

        :param id: Уникальный идентификатор элемента.
        :param code: Машинное имя элемента (например, 'users', 'orders').
        :param name: Человекочитаемое название элемента.
        :param commit: Описание элемента.
        :return: Доменная модель бизнес-элемента.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> BuisnessElementDomain | None:
        """
        Возвращает бизнес-элемент по ID.

        :param id: ID элемента.
        :return: Доменная модель или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, code: str) -> BuisnessElementDomain | None:
        """
        Возвращает бизнес-элемент по его коду.

        :param name: Машинное имя элемента.
        :return: Доменная модель или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        id: int,
        *,
        code: str | None = None,
        name: str | None = None,
        commit: str | None = None,
    ) -> BuisnessElementDomain | None:
        """
        Обновляет данные бизнес-элемента.

        :param id: ID элемента.
        :param code: Новое машинное имя.
        :param name: Новое человекочитаемое название.
        :param commit: Новое описание.
        :return: Обновлённая доменная модель или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> BuisnessElementDomain | None:
        """
        Удаляет бизнес-элемент по ID.

        :param id: ID элемента.
        :return: Возвращает домен бизнес елементов.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[BuisnessElementDomain]:
        """
        Возвращает все бизнес-элементы.

        :return: Список доменных моделей элементов.
        """
        raise NotImplementedError
