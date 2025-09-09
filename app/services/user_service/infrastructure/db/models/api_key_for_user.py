from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class ApiKey(Base):
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        default=text("gen_random_uuid()"),  # для PostgreSQL
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))
    user: Mapped["User"] = relationship("User", back_populates="api_key")
    limit_requests: Mapped[int] = mapped_column(default=200)
