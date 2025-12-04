from domain.exceptions import NotPermissionError, BuisnessElementNotFoundError
from domain.models import UserDomain, Role
from domain.services import BuisnessElementService
from domain.uow import AbstractUnitOfWork
from infrastructure.utils.logger_config import log
from presentation.api.schemas import (
    BuisnessElementResponse,
    ListBuisnessElementResponse,
    CreateBuisnessElementRequest,
    UpdateBuisnessElementRequest,
)


class BuisnessElementHandler:
    def __init__(self, uow: AbstractUnitOfWork):
        self.service = BuisnessElementService(uow)

    async def get_element(self, element_id: int, initiator: UserDomain):
        element = await self.service.get_element_by_id(element_id)
        return BuisnessElementResponse.from_domain(element)

    async def list_elements(self, initiator: UserDomain):
        elements = await self.service.list_elements()
        return ListBuisnessElementResponse.from_domain(elements)

    async def create_element(
        self, element_data: CreateBuisnessElementRequest, initiator: UserDomain
    ):
        if initiator.role != Role.ADMIN:
            raise NotPermissionError("Only admin can create business elements")
        element = await self.service.create_element(
            id=element_data.id,
            code=element_data.buisness_elements,
            name=element_data.name,
        )
        log.info("Created business element: {}", element)
        return BuisnessElementResponse.from_domain(element)

    async def update_element(
        self,
        element_id: int,
        element_data: UpdateBuisnessElementRequest,
        initiator: UserDomain,
    ):
        if initiator.role != Role.ADMIN:
            raise NotPermissionError("Only admin can update business elements")
        element = await self.service.update_element(
            id=element_id,
            name=element_data.name,
            code=element_data.buisness_elements,
        )
        log.info("Updated business element: {}", element)
        return BuisnessElementResponse.from_domain(element)

    async def delete_element(self, element_id: int, initiator: UserDomain):
        if initiator.role != Role.ADMIN:
            raise NotPermissionError("Only admin can delete business elements")
        deleted = await self.service.delete_element(element_id)
        log.info("Deleted business element: {}", deleted)
        return BuisnessElementResponse.from_domain(deleted)
