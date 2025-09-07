from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import (
    AfterValidator,
    AwareDatetime,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
)

from app.services.user_service.schemas.utils import validate_phone

Username = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=25)]
FirstName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=30)]
LastName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=30)]

Money = Annotated[Decimal, Field(gt=0, decimal_places=2)]
PhoneNumber = Annotated[str, AfterValidator(validate_phone)]


class UserSchema(BaseModel):
    username: Username = "JohnDoe"
    first_name: FirstName = "John"
    last_name: LastName = "Doe"
    email: EmailStr = "johndoe@example.com"
    phone_number: PhoneNumber = "+1234567890"
    wallet: Money = Decimal(1000000.00)


class UserCreateSchema(UserSchema): ...


class UserUpdateSchema(BaseModel):
    id: UUID
    username: Username | None = None
    first_name: FirstName | None = None
    last_name: LastName | None = None
    email: EmailStr | None = None
    phone_number: PhoneNumber | None = None
    wallet: Money | None = None


class UserResponseSchema(UserSchema):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: AwareDatetime
    updated_at: AwareDatetime | None = None
