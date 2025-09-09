from abc import abstractmethod
from types import TracebackType
from typing import TYPE_CHECKING, Protocol

from app.services.user_service.domain.entities import User as UserEntity

if TYPE_CHECKING:
    from uuid import UUID

    from app.services.user_service.domain.commands import CreateUserCommand
    from app.services.user_service.infrastructure.db.models import User as UserModel
    from app.services.user_service.schemas import UserUpdateSchema


class UserRepositoryProtocol(Protocol):
    @abstractmethod
    async def add_user(self, user: UserEntity) -> "UserModel": ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> UserEntity: ...

    @abstractmethod
    async def update_user(self, new_user_data: "UserUpdateSchema") -> UserEntity: ...

    @abstractmethod
    async def create_api_key(self, user_id: "UUID") -> str: ...

    @abstractmethod
    async def get_by_api_key(self, api_key: str) -> UserEntity: ...

    @abstractmethod
    async def check_unique_email_and_username(
        self, username: str, email: str
    ) -> tuple[str | None, str | None]: ...


class CreateUserUseCaseProtocol(Protocol):
    @abstractmethod
    async def execute(self, cmd: "CreateUserCommand") -> UserEntity: ...


class UnitOfWorkProtocol(Protocol):
    @abstractmethod
    async def __aenter__(self) -> "UnitOfWorkProtocol": ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: type[BaseException] | None,
        tb: TracebackType | None,
    ) -> None: ...


class EventPublisherProtocol(Protocol):
    async def publish(self, event: dict, routing_key: str) -> None: ...
