from datetime import datetime
from uuid import UUID

from pydantic import Field

from .domain_model import DomainModel


class SessionDomain(DomainModel):
    id: UUID = Field(description="Уникальный идентификатор сессии")
    user_id: int = Field(description="ID пользователя")
    session_token: str = Field(description="Токен сессии (secure random)")
    expires_at: datetime = Field(description="Время окончания сессии")

    created_at: datetime = Field(description="Дата создания сессии")
    last_seen_at: datetime = Field(description="Последняя активность пользователя")

    ip: str | None = Field(default=None, description="IP адрес пользователя")
    user_agent: str | None = Field(default=None, description="User-Agent браузера")
