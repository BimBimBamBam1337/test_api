from domain.exceptions import DepartmentNotFoundError, DepartmentAlreadyExistsError
from domain.entities import Department
from domain.uow import AbstractUnitOfWork


class DepartmentService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.__department_repo = uow.department_repo

    async def create(self, entity: Department) -> Department:
        exists = await self.__department_repo.exists(entity.name)
        if exists:
            raise DepartmentAlreadyExistsError
        department = await self.__department_repo.create(entity)
        return department

    async def get_by_id(self, department_id: int) -> Department:
        department = await self.__department_repo.get_by_id(department_id)
        if department is None:
            raise DepartmentNotFoundError
        return department

    async def change_department(
        self,
        department_id: int,
        name: str | None,
        parent_id: int | None,
    ) -> Department:
        new_department = await self.__department_repo.change_department(
            department_id=department_id, name=name, parent_id=parent_id
        )
        if new_department is None:
            raise DepartmentNotFoundError
        return new_department

    async def update(self, entity: Department) -> Department:
        new_department = await self.__department_repo.update(entity)
        if new_department is None:
            raise DepartmentNotFoundError
        return new_department

    async def delete(
        self,
        department_id: int,
        mode: str,
        reassign_to_department_id: int | None = None,
    ) -> None:

        exists = await self.__department_repo.get_by_id(department_id)
        if not exists:
            raise DepartmentNotFoundError

        if mode == "reassign" and not reassign_to_department_id:
            raise ValueError("reassign_to_department_id is required when mode=reassign")

        await self.__department_repo.delete(
            department_id=department_id,
            mode=mode,
            reassign_to_department_id=reassign_to_department_id,
        )

    async def get_tree(
        self, department_id: int, depth: int = 1, include_employees: bool = True
    ) -> dict:
        department = await self.__department_repo.get_by_id(department_id)
        if department is None:
            raise DepartmentNotFoundError

        async def build_tree(dept_id: int, current_depth: int) -> dict:
            dept = await self.__department_repo.get_by_id(dept_id)
            if not dept:
                return {}

            tree = {
                "id": dept.id,
                "name": dept.name,
                "parent_id": dept.parent_id,
                "children": [],
                "employees": [],
            }

            if include_employees:
                employees = await self.__department_repo.get_employees(dept.id)
                tree["employees"] = [
                    {
                        "id": e.id,
                        "full_name": e.full_name,
                        "position": e.position,
                        "department_id": dept.id,
                        "created_at": e.created_at,
                        "hired_at": e.hired_at,
                    }
                    for e in employees
                ]

            if current_depth < depth:
                children = await self.__department_repo.get_children(dept.id)
                for child in children:
                    tree["children"].append(
                        await build_tree(child.id, current_depth + 1)
                    )

            return tree

        return await build_tree(department_id, 1)
