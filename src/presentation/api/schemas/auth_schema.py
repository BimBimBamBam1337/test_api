from pydantic import BaseModel, Field

from domain.models import TokenType, UserSettings


class AuthLoginRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=UserSettings.USERNAME_MIN_LENGTH,
        max_length=UserSettings.USERNAME_MAX_LENGTH,
        description="Логин пользователя.",
        examples=["admin"],
    )
    password: str = Field(
        ...,
        min_length=UserSettings.PASSWORD_MIN_LENGTH,
        max_length=UserSettings.PASSWORD_MAX_LENGTH,
        description="Пароль пользователя.",
        examples=["pass"],
    )


class AuthLoginResponse(BaseModel):
    access_token: str = Field(..., description="Токен доступа", examples=["token"])
    token_type: TokenType = Field(
        default=TokenType.BEARER, description="Тип токена", examples=["Bearer"]
    )


class AuthRefreshResponse(AuthLoginResponse):
    pass
