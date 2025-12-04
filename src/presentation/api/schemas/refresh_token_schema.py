from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, model_validator

from domain.models.refresh_token_model import RefreshTokenDomain


class RefreshTokenResponse(BaseModel):
    id: int = Field(description="Уникальный ID refresh-токена")
    user_id: int = Field(description="ID пользователя")

    revoked: bool = Field(
        description="Флаг: токен отозван и больше недействителен", examples=[False]
    )
    expires_at: datetime = Field(
        ...,
        description="Время истечения нового access токена",
    )
    created_at: datetime = Field(description="Когда токен был создан")
    updated_at: datetime = Field(description="Когда последний раз обновлялся")

    @classmethod
    def from_domain(cls, refresh_token: RefreshTokenDomain) -> "RefreshTokenResponse":
        return cls(
            id=refresh_token.id,
            user_id=refresh_token.user_id,
            revoked=refresh_token.revoked,
            expires_at=refresh_token.expires_at,
            created_at=refresh_token.created_at,
            updated_at=refresh_token.updated_at,
        )


class ListRefreshTokenResponse(BaseModel):
    refresh_tokens: list[RefreshTokenResponse] = Field(
        ..., description="Список токенов"
    )
    total: int = Field(..., description="Кол-во токенов")

    @classmethod
    def from_domain(
        cls, refresh_tokens: list[RefreshTokenDomain]
    ) -> "ListRefreshTokenResponse":
        return cls(
            refresh_tokens=[
                RefreshTokenResponse.from_domain(refresh_token)
                for refresh_token in refresh_tokens
            ],
            total=len(refresh_tokens),
        )


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(
        ...,
        description="Refresh токен, выданный ранее",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )


class CreateRefreshTokenResponse(BaseModel):
    id: int = Field(description="ID refresh-токена", examples=[1])
    user_id: int = Field(description="ID пользователя", examples=[5])

    token_hash: str = Field(
        description="Сам refresh токен (отдаётся только один раз)",
        examples=["eyJhbGciOi..."],
    )

    expires_at: datetime = Field(description="Время истечения refresh-токена")
    created_at: datetime = Field(description="Когда токен создан")
    updated_at: datetime = Field(description="Когда последний раз обновлялся")


class UpdateRefreshTokenResponse(BaseModel):
    refresh_token: str = Field(
        description="Обновлённый refresh-токен",
        examples=["eyJhbGciOi..."],
    )
    access_token: str = Field(
        description="Свежий access-токен",
        examples=["eyJ0eXAiOi..."],
    )
    expires_at: datetime = Field(
        description="Когда истекает refresh-токен",
    )

    @model_validator(mode="after")
    def validate_params(self):
        if (
            self.refresh_token is None
            and self.access_token is None
            and self.expires_at is None
        ):
            raise ValidationError(
                "At least one of name or description must be provided"
            )
        return self
