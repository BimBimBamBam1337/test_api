import pytest
from infra.database.repositories import DepartmentRepository, EmployeeRepository
from domain.entities import Department, Employee


@pytest.mark.asyncio
async def test_create_department(session):
    repo = DepartmentRepository(session)

    department = Department.create(name="IT", parent_id=None)
    created = await repo.create(department)

    await session.commit()

    assert created.id is not None
    assert created.name == "IT"


@pytest.mark.asyncio
async def test_department_exists(session):
    repo = DepartmentRepository(session)

    department = Department.create(name="HR", parent_id=None)
    await repo.create(department)

    exists = await repo.exists("HR")
    await session.commit()
    assert exists is True


@pytest.mark.asyncio
async def test_update_department(session):
    repo = DepartmentRepository(session)

    department = Department.create(name="Old", parent_id=None)
    created = await repo.create(department)

    created.name = "New"
    updated = await repo.update(created)
    await session.commit()
    assert updated.name == "New"


@pytest.mark.asyncio
async def test_delete_cascade(session):
    dept_repo = DepartmentRepository(session)
    emp_repo = EmployeeRepository(session)

    parent = await dept_repo.create(Department.create(name="Parent", parent_id=None))
    child = await dept_repo.create(Department.create(name="Child", parent_id=parent.id))

    employee = Employee.create(
        full_name="John",
        position="Dev",
        department_id=child.id,
        hired_at=None,
    )

    await emp_repo.create(employee)

    await dept_repo.delete(parent.id, mode="cascade", reassign_to_department_id=None)
    await session.commit()
    assert await dept_repo.get_by_id(parent.id) is None
    assert await dept_repo.get_by_id(child.id) is None


@pytest.mark.asyncio
async def test_delete_reassign(session):
    dept_repo = DepartmentRepository(session)
    emp_repo = EmployeeRepository(session)

    parent = await dept_repo.create(Department.create(name="A", parent_id=None))
    target = await dept_repo.create(Department.create(name="B", parent_id=None))

    employee = Employee.create(
        full_name="Mike",
        position="Dev",
        department_id=parent.id,
        hired_at=None,
    )

    created_emp = await emp_repo.create(employee)

    await dept_repo.delete(
        parent.id,
        mode="reassign",
        reassign_to_department_id=target.id,
    )

    updated_emp = await emp_repo.get_by_id(created_emp.id)
    await session.commit()
    assert updated_emp.department_id == target.id
