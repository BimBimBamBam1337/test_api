from fastapi import APIRouter, Depends, Path

from domain.models import UserDomain
from presentation.api.dependencies import (
    get_user_from_verify_token,
    get_session_handler,
)
from presentation.api.handlers import SessionHandler
from presentation.api.schemas import (
    SessionResponse,
    CreateSessionResponse,
)

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.get(
    "",
    summary="Получение списка активных сессий текущего пользователя",
    response_description="Возвращает список активных сессий.",
    response_model=list[SessionResponse],
)
async def list_sessions_handler(
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: SessionHandler = Depends(get_session_handler),
):
    return await handler.list_user_sessions(user.id, requester=user)


@router.get(
    "/{session_id}",
    summary="Получение информации о конкретной сессии",
    response_model=SessionResponse,
)
async def get_session_handler(
    session_id: str = Path(..., description="UUID сессии"),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: SessionHandler = Depends(get_session_handler),
):
    return await handler.get_session(session_id=session_id, requester=user)


@router.delete(
    "/{session_id}",
    summary="Закрытие указанной сессии",
    response_description="Возвращает закрытую сессию.",
    response_model=SessionResponse,
)
async def delete_session_handler(
    session_id: str = Path(..., description="UUID сессии"),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: SessionHandler = Depends(get_session_handler),
):
    return await handler.delete_session(session_id=session_id, requester=user)


@router.delete(
    "",
    summary="Закрыть все активные сессии пользователя",
    response_description="Возвращает список закрытых сессий.",
    response_model=list[SessionResponse],
)
async def delete_all_sessions_handler(
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: SessionHandler = Depends(get_session_handler),
):
    return await handler.delete_user_sessions(user.id, requester=user)
