from fastapi import Response, status
from fastapi.responses import JSONResponse
from jose import JWTError

from config import settings
from domain.exceptions import UserInvalidPasswordError
from domain.models import UserDomain
from domain.services import UserService
from domain.uow import AbstractUnitOfWork
from infrastructure.utils.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from presentation.api.schemas import (
    AuthLoginRequest,
    AuthLoginResponse,
    AuthRefreshResponse,
)


class AuthHandler:
    def __init__(self, uow: AbstractUnitOfWork):
        self.user_service = UserService(uow)

    async def login(self, auth: AuthLoginRequest) -> JSONResponse:
        user = await self.user_service.get_user_by_username(auth.username)
        if not user.verify_password(auth.password):
            raise UserInvalidPasswordError()
        response = JSONResponse(
            content=AuthLoginResponse(
                access_token=create_access_token(
                    {"user_id": user.id}, settings.secret_key
                )
            ).model_dump(),
            status_code=200,
        )
        response.set_cookie(
            key="refresh_token",
            value=create_refresh_token({"user_id": user.id}, settings.secret_key),
            httponly=True,
            secure=True,
            samesite="none",
            max_age=int(settings.refresh_token_expire.total_seconds()),
        )
        return response

    async def logout(self, user: UserDomain) -> Response:
        response = Response(status_code=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(key="refresh_token")
        return response

    async def refresh(self, refresh_token: str | None) -> JSONResponse:
        if not refresh_token:
            raise JWTError("Refresh token not found")
        payload = decode_token(refresh_token, settings.secret_key, "refresh")
        user_id = payload.get("user_id")
        if user_id is None:
            raise JWTError("Invalid token type")
        user = await self.user_service.get_user_by_id(user_id)
        return JSONResponse(
            content=AuthRefreshResponse(
                access_token=create_access_token(
                    {"user_id": user.id}, settings.secret_key
                )
            ).model_dump(),
            status_code=200,
        )

    async def status(self, user: UserDomain) -> Response:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
