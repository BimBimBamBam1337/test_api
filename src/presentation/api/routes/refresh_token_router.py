from fastapi import APIRouter, Body, Depends, Path

from domain.models import UserDomain
from presentation.api.dependencies import (
    get_user_from_verify_token,
    get_refresh_token_handler,
)
from presentation.api.handlers import RefreshTokenHandler
from presentation.api.schemas import (
    RefreshTokenResponse,
    ListRefreshTokenResponse,
    CreateRefreshTokenResponse,
    UpdateRefreshTokenResponse,
)

router = APIRouter(prefix="/refresh-tokens", tags=["Refresh Tokens"])


@router.get(
    "",
    summary="Список refresh-токенов текущего пользователя",
    response_model=ListRefreshTokenResponse,
)
async def list_refresh_tokens_handler(
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: RefreshTokenHandler = Depends(get_refresh_token_handler),
):
    return await handler.list_tokens(user)


# @router.post(
#     "/refresh",
#     summary="Обновление refresh-токена",
#     response_model=UpdateRefreshTokenResponse,
# )
# async def refresh_token_handler(
#     data: RefreshTokenRequest = Body(...),
#     handler: RefreshTokenHandler = Depends(get_refresh_token_handler),
# ):
#     """
#     Обновляет refresh-токен и возвращает новый access token.
#     """
#     return await handler.refresh_token(refresh_token=data.refresh_token)


@router.delete(
    "/{token_id}",
    summary="Отзыв refresh-токена",
    response_model=RefreshTokenResponse,
)
async def revoke_refresh_token_handler(
    token_id: int = Path(..., description="ID refresh-токена"),
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: RefreshTokenHandler = Depends(get_refresh_token_handler),
):
    return await handler.revoke_token(token_id=token_id, initiator=user)


@router.delete(
    "",
    summary="Отзыв всех refresh-токенов текущего пользователя",
    response_model=int,
    response_description="Количество отозванных токенов",
)
async def revoke_all_tokens_handler(
    user: UserDomain = Depends(get_user_from_verify_token),
    handler: RefreshTokenHandler = Depends(get_refresh_token_handler),
):
    return await handler.revoke_user_tokens(user.id, initiator=user)
