from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from app.services.user_service.domain.entities import User as UserEntity
from app.services.user_service.domain.exceptions import (
    EmailAlreadyExists,
    UsernameAlreadyExists,
)
from app.services.user_service.infrastructure.messaging.events import UserCreated

if TYPE_CHECKING:
    from app.services.user_service.domain.commands import CreateUserCommand
    from app.services.user_service.domain.ports import (
        EventPublisherProtocol,
        UnitOfWorkProtocol,
        UserRepositoryProtocol,
    )


class CreateUserUseCase:
    def __init__(
        self,
        uow: "UnitOfWorkProtocol",
        repo: "UserRepositoryProtocol",
        event_publisher: "EventPublisherProtocol",
    ) -> None:
        self.uow = uow
        self.repo = repo
        self.event_publisher = event_publisher

    async def execute(self, cmd: "CreateUserCommand") -> UserEntity:
        async with self.uow:
            existing = await self.repo.get_by_email(cmd.email)
            if existing:
                raise EmailAlreadyExists(email=cmd.email)

            existing = await self.repo.get_by_username(cmd.username)
            if existing:
                raise UsernameAlreadyExists(username=cmd.username)

            user = UserEntity(
                username=cmd.username,
                first_name=cmd.first_name,
                last_name=cmd.last_name,
                email=cmd.email,
                phone_number=cmd.phone_number,
                wallet=cmd.wallet,
            )

            model = await self.repo.add(user)

            event = UserCreated(
                user_id=user.id,
                username=user.username,
                email=user.email,
                phone_number=user.phone_number,
                occurred_at=datetime.now(UTC),
                correlation_id=str(uuid4()),
            )
            await self.event_publisher.publish(
                event.model_dump(),
                routing_key="user.created",
            )

            return model.to_entity()
