from fastapi import APIRouter, Body, Path, Depends
from domain.models import UserDomain
from presentation.api.dependencies import (
    get_buisness_element_handler,
    get_user_from_verify_token,
)
from presentation.api.handlers import BuisnessElementHandler
from presentation.api.schemas import (
    BuisnessElementResponse,
    ListBuisnessElementResponse,
    CreateBuisnessElementRequest,
    UpdateBuisnessElementRequest,
)

router = APIRouter(prefix="/buisness-elements", tags=["Buisness Elements"])


@router.get(
    "",
    summary="Список всех бизнес-элементов",
    response_model=ListBuisnessElementResponse,
)
async def list_buisness_elements_handler(
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: BuisnessElementHandler = Depends(get_buisness_element_handler),
):
    return await handler.list_elements(user)


@router.post(
    "",
    summary="Создание нового бизнес-элемента",
    response_model=BuisnessElementResponse,
)
async def create_buisness_element_handler(
    element_data: CreateBuisnessElementRequest = Body(...),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: BuisnessElementHandler = Depends(get_buisness_element_handler),
):
    return await handler.create_element(element_data=element_data, initiator=user)


@router.patch(
    "/{element_id}",
    summary="Обновление бизнес-элемента",
    response_model=BuisnessElementResponse,
)
async def update_buisness_element_handler(
    element_id: int = Path(..., description="ID бизнес-элемента"),
    element_data: UpdateBuisnessElementRequest = Body(...),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: BuisnessElementHandler = Depends(get_buisness_element_handler),
):
    return await handler.update_element(
        element_id=element_id, element_data=element_data, initiator=user
    )


@router.delete(
    "/{element_id}",
    summary="Удаление бизнес-элемента",
    response_model=BuisnessElementResponse,
)
async def delete_buisness_element_handler(
    element_id: int = Path(..., description="ID бизнес-элемента"),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: BuisnessElementHandler = Depends(get_buisness_element_handler),
):
    return await handler.delete_element(element_id=element_id, initiator=user)
