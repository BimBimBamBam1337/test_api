from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from domain.models import AccessRoleRuleDomain
from domain.repositories import AbstractAccessRoleRuleRepository
from infrastructure.database.models import AccessRoleRuleORM


class AccessRoleRuleRepository(AbstractAccessRoleRuleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, id: int) -> bool:
        result = await self.session.execute(
            select(1).where(AccessRoleRuleORM.id == id).limit(1)
        )
        return result.scalar() is not None

    async def create(
        self,
        *,
        id: int,
        role_id: int,
        element_id: int,
        read_permission: bool = False,
        read_all_permission: bool = False,
        create_permission: bool = False,
        update_permission: bool = False,
        update_all_permission: bool = False,
        delete_permission: bool = False,
        delete_all_permission: bool = False,
    ) -> AccessRoleRuleDomain:
        rule_orm = AccessRoleRuleORM(
            id=id,
            role_id=role_id,
            element_id=element_id,
            read_permission=read_permission,
            read_all_permission=read_all_permission,
            create_permission=create_permission,
            update_permission=update_permission,
            update_all_permission=update_all_permission,
            delete_permission=delete_permission,
            delete_all_permission=delete_all_permission,
        )
        self.session.add(rule_orm)
        await self.session.flush()
        return rule_orm.to_domain()

    async def get_by_id(self, id: int) -> AccessRoleRuleDomain | None:
        rule_orm = await self.session.get(AccessRoleRuleORM, id)
        return rule_orm.to_domain() if rule_orm else None

    async def get_by_role_and_element(
        self, role_id: int, element_id: int
    ) -> AccessRoleRuleDomain | None:
        result = await self.session.execute(
            select(AccessRoleRuleORM)
            .where(
                AccessRoleRuleORM.role_id == role_id,
                AccessRoleRuleORM.element_id == element_id,
            )
            .limit(1)
        )
        rule_orm: AccessRoleRuleORM | None = result.scalar_one_or_none()
        return rule_orm.to_domain() if rule_orm else None

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
        values = {}
        if read_permission is not None:
            values["read_permission"] = read_permission
        if read_all_permission is not None:
            values["read_all_permission"] = read_all_permission
        if create_permission is not None:
            values["create_permission"] = create_permission
        if update_permission is not None:
            values["update_permission"] = update_permission
        if update_all_permission is not None:
            values["update_all_permission"] = update_all_permission
        if delete_permission is not None:
            values["delete_permission"] = delete_permission
        if delete_all_permission is not None:
            values["delete_all_permission"] = delete_all_permission

        result = await self.session.execute(
            update(AccessRoleRuleORM)
            .where(AccessRoleRuleORM.id == id)
            .values(**values)
            .returning(AccessRoleRuleORM)
        )
        await self.session.flush()
        rule_orm: AccessRoleRuleORM | None = result.scalar_one_or_none()
        return rule_orm.to_domain() if rule_orm else None

    async def delete(self, id: int) -> AccessRoleRuleDomain | None:
        result = await self.session.execute(
            delete(AccessRoleRuleORM)
            .where(AccessRoleRuleORM.id == id)
            .returning(AccessRoleRuleORM)
        )
        await self.session.flush()
        access_role_rules_orm: AccessRoleRuleORM | None = result.scalar_one_or_none()
        return access_role_rules_orm.to_domain() if access_role_rules_orm else None

    async def get_all(self) -> list[AccessRoleRuleDomain]:
        result = await self.session.execute(select(AccessRoleRuleORM))
        rules_orm = result.scalars().all()
        return [rule.to_domain() for rule in rules_orm]
