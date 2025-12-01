from datetime import datetime
from pydantic import Field

from .domain_model import DomainModel


class RefreshTokenDomain(DomainModel):
    id: int = Field(description="Уникальный ID refresh-токена")
    user_id: int = Field(description="ID пользователя")

    token_hash: str = Field(
        description="Хэш refresh-токена (сам токен хранить в чистом виде нельзя!)"
    )

    revoked: bool = Field(
        description="Флаг: токен отозван и больше недействителен", examples=[False]
    )

    expires_at: datetime = Field(description="Время истечения refresh-токена")

    created_at: datetime = Field(description="Когда токен был создан")
    updated_at: datetime = Field(description="Когда последний раз обновлялся")
