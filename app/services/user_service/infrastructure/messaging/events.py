from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreated(BaseModel):
    event_type: str = "UserCreated.v1"
    user_id: UUID
    username: str
    email: str
    phone_number: str
    occurred_at: datetime
    correlation_id: str
