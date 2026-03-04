import pytest

from infra.database.repositories import EmployeeRepository, DepartmentRepository
from domain.entities import Employee, Department


@pytest.mark.asyncio
async def test_create_employee(session):
    dept_repo = DepartmentRepository(session)
    emp_repo = EmployeeRepository(session)

    department = await dept_repo.create(Department.create(name="IT", parent_id=None))

    employee = Employee.create(
        full_name="John Doe",
        position="Backend",
        department_id=department.id,
        hired_at=None,
    )

    created = await emp_repo.create(employee)
    await session.commit()
    assert created.id is not None
    assert created.full_name == "John Doe"
    assert created.department_id == department.id


@pytest.mark.asyncio
async def test_employee_exists(session):
    dept_repo = DepartmentRepository(session)
    emp_repo = EmployeeRepository(session)

    department = await dept_repo.create(Department.create(name="HR", parent_id=None))

    employee = await emp_repo.create(
        Employee.create(
            full_name="Alice",
            position="HR",
            department_id=department.id,
            hired_at=None,
        )
    )

    exists = await emp_repo.exists(employee.id)
    await session.commit()
    assert exists is True
    assert await emp_repo.exists(99999) is False


@pytest.mark.asyncio
async def test_get_employee_by_id(session):
    dept_repo = DepartmentRepository(session)
    emp_repo = EmployeeRepository(session)

    department = await dept_repo.create(
        Department.create(name="Finance", parent_id=None)
    )

    employee = await emp_repo.create(
        Employee.create(
            full_name="Bob",
            position="Accountant",
            department_id=department.id,
            hired_at=None,
        )
    )

    found = await emp_repo.get_by_id(employee.id)
    await session.commit()
    assert found is not None
    assert found.id == employee.id
    assert found.full_name == "Bob"


@pytest.mark.asyncio
async def test_update_employee(session):
    dept_repo = DepartmentRepository(session)
    emp_repo = EmployeeRepository(session)

    department = await dept_repo.create(Department.create(name="QA", parent_id=None))

    employee = await emp_repo.create(
        Employee.create(
            full_name="Charlie",
            position="Tester",
            department_id=department.id,
            hired_at=None,
        )
    )

    employee.full_name = "Charlie Updated"
    employee.position = "Senior Tester"

    updated = await emp_repo.update(employee)
    await session.commit()
    assert updated.full_name == "Charlie Updated"
    assert updated.position == "Senior Tester"


@pytest.mark.asyncio
async def test_delete_employee(session):
    dept_repo = DepartmentRepository(session)
    emp_repo = EmployeeRepository(session)

    department = await dept_repo.create(
        Department.create(name="Support", parent_id=None)
    )

    employee = await emp_repo.create(
        Employee.create(
            full_name="David",
            position="Support",
            department_id=department.id,
            hired_at=None,
        )
    )

    await emp_repo.delete(employee.id)
    await session.commit()
    assert await emp_repo.get_by_id(employee.id) is None
