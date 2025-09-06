from abc import abstractmethod
from types import TracebackType
from typing import TYPE_CHECKING, Protocol

from app.services.user_service.domain.entities import User as UserEntity

if TYPE_CHECKING:
    from app.services.user_service.domain.commands import CreateUserCommand
    from app.services.user_service.infrastructure.db.models import User as UserModel


class UserRepositoryProtocol(Protocol):
    @abstractmethod
    async def add(self, user: UserEntity) -> "UserModel": ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> UserEntity | None: ...


class CreateUserUseCaseProtocol(Protocol):
    @abstractmethod
    async def execute(self, cmd: "CreateUserCommand") -> "UserModel": ...


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
