from decimal import Decimal

from sqlalchemy import Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import TimestampMixin


class Product(TimestampMixin, Base):
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    def __str__(self) -> str:
        return f"Product - {self.name} | ID: {self.id}"

    def __repr__(self) -> str:
        return str(self)
