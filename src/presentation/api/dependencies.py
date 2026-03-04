from typing import AsyncGenerator
from loguru import logger
from fastapi import Depends

from domain.uow import AbstractUnitOfWork
from infra.database.session import SessionFactory
from infra.database.uow import SQLAlchemyUnitOfWork
from presentation.api.handlers import DepartmentHandler, EmployeeHandler


async def get_uow() -> AsyncGenerator[SQLAlchemyUnitOfWork]:
    async with SQLAlchemyUnitOfWork(SessionFactory) as uow:
        logger.info("SQLAlchemyUnitOfWork started transaction")
        yield uow
        logger.info("SQLAlchemyUnitOfWork finished transaction")


async def get_department_handler(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> DepartmentHandler:
    return DepartmentHandler(uow)


async def get_employee_handler(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> EmployeeHandler:
    return EmployeeHandler(uow)
