from fastapi import APIRouter, Depends, Body, HTTPException, Path, Query, status
from datetime import date

from domain.exceptions import DepartmentNotFoundError, DepartmentAlreadyExistsError
from presentation.api.dependencies import (
    get_department_handler,
    get_employee_handler,
)
from presentation.api.handlers import (
    DepartmentHandler,
    EmployeeHandler,
)
from presentation.api.schemas import (
    CreateDepartmentRequest,
    UpdateDepartmentRequest,
    CreateEmployeeRequest,
    DepartmentTreeResponse,
    EmployeeResponse,
)

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post(
    "",
    summary="Создать подразделение",
    response_model=DepartmentTreeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_department(
    data: CreateDepartmentRequest = Body(...),
    handler: DepartmentHandler = Depends(get_department_handler),
):
    try:
        return await handler.create(
            name=data.name,
            parent_id=data.parent_id,
        )
    except DepartmentAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Employee already exist")


@router.post(
    "/{department_id}/employees",
    summary="Создать сотрудника в подразделении",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_employee_in_department(
    department_id: int = Path(...),
    data: CreateEmployeeRequest = Body(...),
    handler: EmployeeHandler = Depends(get_employee_handler),
):
    try:
        return await handler.create(
            department_id=department_id,
            full_name=data.full_name,
            position=data.position,
            hired_at=data.hired_at,
        )
    except DepartmentNotFoundError:
        raise HTTPException(status_code=404, detail="Department not found")


@router.get(
    "/{department_id}",
    summary="Получить подразделение с деревом и сотрудниками",
    response_model=DepartmentTreeResponse,
)
async def get_department_tree(
    department_id: int = Path(...),
    depth: int = Query(1, ge=1, le=5),
    include_employees: bool = Query(True),
    handler: DepartmentHandler = Depends(get_department_handler),
):
    try:
        return await handler.get_tree(
            department_id=department_id,
            depth=depth,
            include_employees=include_employees,
        )
    except DepartmentNotFoundError:
        raise HTTPException(status_code=404, detail="Department not found")


@router.patch(
    "/{department_id}",
    summary="Обновить подразделение (сменить имя или parent)",
)
async def update_department(
    department_id: int = Path(...),
    data: UpdateDepartmentRequest = Body(...),
    handler: DepartmentHandler = Depends(get_department_handler),
):
    try:
        return await handler.change(
            department_id=department_id,
            name=data.name,
            parent_id=data.parent_id,
        )
    except DepartmentNotFoundError:
        raise HTTPException(status_code=404, detail="Department not found")


@router.delete(
    "/{department_id}",
    summary="Удалить подразделение",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_department(
    department_id: int = Path(...),
    mode: str = Query(..., pattern="^(cascade|reassign)$"),
    reassign_to_department_id: int | None = Query(None),
    handler: DepartmentHandler = Depends(get_department_handler),
):
    try:
        await handler.delete(
            department_id=department_id,
            mode=mode,
            reassign_to_department_id=reassign_to_department_id,
        )
    except DepartmentNotFoundError:
        raise HTTPException(status_code=404, detail="Department not found")
