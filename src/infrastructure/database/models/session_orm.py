from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import BIGINT, BOOLEAN, DateTime, String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from domain.models import SessionDomain
from .base import BaseORM


class SessionORM(BaseORM):
    __tablename__ = "sessions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id"), nullable=False)
    session_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        BOOLEAN, nullable=False, server_default=expression.true()
    )

    def __repr__(self) -> str:
        return f"SessionORM(id={self.id!r}, user_id={self.user_id!r}, token={self.session_token!r})"

    def to_domain(self) -> SessionDomain:
        return SessionDomain.model_validate(self)
