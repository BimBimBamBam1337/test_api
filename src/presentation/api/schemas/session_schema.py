from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ValidationError, model_validator

from domain.models import SessionDomain


class SessionResponse(BaseModel):
    id: UUID = Field(description="Уникальный идентификатор сессии", examples=[1])
    user_id: int = Field(description="ID пользователя", examples=[2])
    expires_at: datetime = Field(description="Время окончания сессии")

    last_seen_at: datetime = Field(description="Последняя активность пользователя")

    @classmethod
    def from_domain(cls, session: SessionDomain) -> "SessionResponse":
        return cls(
            id=session.id,
            user_id=session.user_id,
            expires_at=session.expires_at,
            last_seen_at=session.last_seen_at,
        )


class CreateSessionResponse(BaseModel):
    id: UUID = Field(description="Уникальный идентификатор сессии", examples=[1])
    user_id: int = Field(description="ID пользователя", examples=[2])
    session_token: str = Field(description="Токен сессии (secure random)")
    expires_at: datetime = Field(description="Время окончания сессии")

    last_seen_at: datetime = Field(description="Последняя активность пользователя")

    ip: str | None = Field(default=None, description="IP адрес пользователя")
    user_agent: str | None = Field(default=None, description="User-Agent браузера")
