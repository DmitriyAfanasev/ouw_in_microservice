from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CreateUserCommand:
    # id: UUID
    username: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    wallet: Decimal
