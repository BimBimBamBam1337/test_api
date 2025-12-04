from abc import ABC, abstractmethod

from domain.models import AccessRoleRuleDomain
from infrastructure.utils.profiler import ProfileABCMeta


class AbstractAccessRoleRuleRepository(ABC, metaclass=ProfileABCMeta):
    @abstractmethod
    async def exists(self, id: int) -> bool:
        """
        Проверяет, существует ли правила для роли по ID.

        :param id: ID пользователя.
        :return: True, если пользователь существует, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        *,
        id: int,
        role: str,
        element_id: int,
        read_permission: bool = False,
        read_all_permission: bool = False,
        create_permission: bool = False,
        update_permission: bool = False,
        update_all_permission: bool = False,
        delete_permission: bool = False,
        delete_all_permission: bool = False,
    ) -> AccessRoleRuleDomain:
        """
        Создаёт правило доступа для роли к бизнес-элементу.

        :param id: Уникальный идентификатор правила.
        :param role: Наименование роли.
        :param element_id: ID бизнес-элемента.
        :param read_permission: Разрешение на чтение собственных объектов.
        :param read_all_permission: Разрешение на чтение всех объектов.
        :param create_permission: Разрешение на создание объектов.
        :param update_permission: Разрешение на изменение собственных объектов.
        :param update_all_permission: Разрешение на изменение всех объектов.
        :param delete_permission: Разрешение на удаление собственных объектов.
        :param delete_all_permission: Разрешение на удаление всех объектов.
        :return: Доменная модель правила доступа.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> AccessRoleRuleDomain | None:
        """
        Возвращает правило доступа по ID.

        :param id: ID правила.
        :return: Доменная модель или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_role_and_element(
        self, role: str, element_id: int
    ) -> AccessRoleRuleDomain | None:
        """
        Возвращает правило доступа по роли и бизнес-элементу.

        :param role: Наименование роли.
        :param element_id: ID бизнес-элемента.
        :return: Доменная модель или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        id: int,
        *,
        read_permission: bool | None = None,
        read_all_permission: bool | None = None,
        create_permission: bool | None = None,
        update_permission: bool | None = None,
        update_all_permission: bool | None = None,
        delete_permission: bool | None = None,
        delete_all_permission: bool | None = None,
    ) -> AccessRoleRuleDomain | None:
        """
        Обновляет правило доступа.

        :param id: ID правила.
        :return: Обновлённая доменная модель или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> AccessRoleRuleDomain | None:
        """
        Удаляет правило доступа по ID.

        :param id: ID правила.
        :return: True, если удаление прошло успешно, иначе False.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[AccessRoleRuleDomain]:
        """
        Возвращает все правила доступа.

        :return: Список доменных моделей правил доступа.
        """
        raise NotImplementedError
