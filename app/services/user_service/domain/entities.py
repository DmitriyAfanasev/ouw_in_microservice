from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from .exceptions import EmailInStopList, NotEmailError, NotNameError


@dataclass
class User:
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str
    wallet: Decimal
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.username.strip():
            raise NotNameError(name=self.username)

        if not self.email.strip():
            raise NotEmailError(email=self.email)

        if self.email.endswith("@stop.fu"):
            raise EmailInStopList(email=self.email)
