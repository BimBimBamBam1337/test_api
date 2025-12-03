from datetime import datetime
from sqlalchemy import BIGINT, BOOLEAN, DateTime, String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from domain.models import RefreshTokenDomain
from .base import BaseORM


class RefreshTokenORM(BaseORM):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id"), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    revoked: Mapped[bool] = mapped_column(
        BOOLEAN, nullable=False, server_default=expression.func(False)
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"RefreshTokenORM(id={self.id!r}, user_id={self.user_id!r}, revoked={self.revoked!r})"

    def to_domain(self) -> RefreshTokenDomain:
        return RefreshTokenDomain.model_validate(self)
