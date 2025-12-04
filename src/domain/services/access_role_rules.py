from domain.exceptions import (
    AccessRoleRuleNotFoundError,
    AccessRoleRuleAlreadyExistsError,
)
from domain.models import AccessRoleRuleDomain
from domain.uow import AbstractUnitOfWork


class AccessRoleRuleService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.__rule_repo = uow.access_role_rules_repo

    async def exists(self, id: int) -> bool:
        """
        Проверяет, существует ли правило доступа с указанным ID.

        :param id: ID правила.
        :return: True, если правило существует, иначе False.
        """
        return await self.__rule_repo.exists(id)

    async def create_rule(
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
        Создаёт новое правило доступа для роли к бизнес-элементу.

        :param id: Уникальный идентификатор правила.
        :param role: Имя роли.
        :param element_id: ID бизнес-элемента.
        :return: Доменная модель правила доступа.
        :raise AccessRoleRuleAlreadyExistsError: Если правило для данной роли и элемента уже существует.
        """
        existing = await self.__rule_repo.get_by_role_and_element(role, element_id)
        if existing is not None:
            raise AccessRoleRuleAlreadyExistsError(role=role, element_id=element_id)

        rule = await self.__rule_repo.create(
            id=id,
            role=role,
            element_id=element_id,
            read_permission=read_permission,
            read_all_permission=read_all_permission,
            create_permission=create_permission,
            update_permission=update_permission,
            update_all_permission=update_all_permission,
            delete_permission=delete_permission,
            delete_all_permission=delete_all_permission,
        )
        return rule

    async def get_rule_by_id(self, id: int) -> AccessRoleRuleDomain:
        """
        Возвращает правило доступа по ID.

        :param id: ID правила.
        :return: Доменная модель правила доступа.
        :raise AccessRoleRuleNotFoundError: Если правило не найдено.
        """
        rule = await self.__rule_repo.get_by_id(id)
        if rule is None:
            raise AccessRoleRuleNotFoundError(id=id)
        return rule

    async def get_rule_by_role_and_element(
        self, role: str, element_id: int
    ) -> AccessRoleRuleDomain:
        """
        Возвращает правило доступа по роли и бизнес-элементу.

        :param role_id: ID роли.
        :param element_id: ID бизнес-элемента.
        :return: Доменная модель правила доступа.
        :raise AccessRoleRuleNotFoundError: Если правило не найдено.
        """
        rule = await self.__rule_repo.get_by_role_and_element(role, element_id)
        if rule is None:
            raise AccessRoleRuleNotFoundError(role=role, element_id=element_id)
        return rule

    async def update_rule(
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
    ) -> AccessRoleRuleDomain:
        """
        Обновляет правило доступа.

        :param id: ID правила.
        :return: Обновлённая доменная модель правила доступа.
        :raise AccessRoleRuleNotFoundError: Если правило не найдено.
        """
        updated = await self.__rule_repo.update(
            id,
            read_permission=read_permission,
            read_all_permission=read_all_permission,
            create_permission=create_permission,
            update_permission=update_permission,
            update_all_permission=update_all_permission,
            delete_permission=delete_permission,
            delete_all_permission=delete_all_permission,
        )
        if updated is None:
            raise AccessRoleRuleNotFoundError(id=id)
        return updated

    async def delete_rule(self, id: int) -> AccessRoleRuleDomain:
        """
        Удаляет правило доступа по ID.

        :param id: ID правила.
        :return: True, если удаление прошло успешно.
        :raise AccessRoleRuleNotFoundError: Если правило не найдено.
        """
        deleted = await self.__rule_repo.delete(id)
        if not deleted:
            raise AccessRoleRuleNotFoundError(id=id)
        return deleted

    async def list_rules(self) -> list[AccessRoleRuleDomain]:
        """
        Возвращает все правила доступа.

        :return: Список доменных моделей правил доступа.
        """
        return await self.__rule_repo.get_all()
