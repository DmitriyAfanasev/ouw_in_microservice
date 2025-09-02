from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class UserServiceError(Exception, ABC):
    pass


@dataclass(frozen=True, eq=False)
class NotNameError(UserServiceError):
    name: str

    @property
    def message(self) -> str:
        return "Name cannot be empty"


@dataclass(frozen=True, eq=False)
class NotEmailError(UserServiceError):
    email: str

    @property
    def message(self) -> str:
        return "Email cannot be empty"


@dataclass(frozen=True, eq=False)
class EmailInStopList(UserServiceError):
    email: str

    @property
    def message(self) -> str:
        return "Email from is Абубадоссия in stop list"


@dataclass(frozen=True, eq=False)
class UseCaseError(Exception):
    """Base for domain errors."""


@dataclass(frozen=True, eq=False)
class EmailAlreadyExists(UseCaseError):
    email: str

    @property
    def message(self) -> str:
        return f"Email {self.email!r} already exists"


@dataclass(frozen=True, eq=False)
class UsernameAlreadyExists(UseCaseError):
    username: str

    @property
    def message(self) -> str:
        return f"Username {self.username!r} already exists"
