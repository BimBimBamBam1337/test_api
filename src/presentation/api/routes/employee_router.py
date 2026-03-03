from fastapi import APIRouter, Depends, Body, Path

from presentation.api.dependencies import get_employee_handler
from presentation.api.handlers import EmployeeHandler
from presentation.api.schemas import (
    CreateEmployeeRequest,
    UpdateEmployeeRequest,
    EmployeeResponse,
)

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post(
    "",
    summary="Создание сотрудника",
    response_model=EmployeeResponse,
)
async def create_employee_handler(
    data: CreateEmployeeRequest = Body(...),
    handler: EmployeeHandler = Depends(get_employee_handler),
):
    return await handler.create(
        employee_id=data.id,
        department_id=data.department_id,
        full_name=data.full_name,
        position=data.position,
    )


@router.get(
    "/{employee_id}",
    summary="Получение сотрудника по ID",
    response_model=EmployeeResponse,
)
async def get_employee_handler_route(
    employee_id: int = Path(...),
    handler: EmployeeHandler = Depends(get_employee_handler),
):
    return await handler.get(employee_id)


@router.patch(
    "/{employee_id}",
    summary="Обновление сотрудника",
    response_model=EmployeeResponse,
)
async def update_employee_handler(
    employee_id: int = Path(...),
    data: UpdateEmployeeRequest = Body(...),
    handler: EmployeeHandler = Depends(get_employee_handler),
):
    return await handler.update(
        employee_id=employee_id,
        department_id=data.department_id,
        full_name=data.full_name,
        position=data.position,
    )


@router.delete(
    "/{employee_id}",
    summary="Удаление сотрудника",
)
async def delete_employee_handler(
    employee_id: int = Path(...),
    handler: EmployeeHandler = Depends(get_employee_handler),
):
    await handler.delete(employee_id)
    return {"status": "deleted"}
