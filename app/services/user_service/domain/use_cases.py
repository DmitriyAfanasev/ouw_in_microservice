from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from faststream.rabbit import ExchangeType, RabbitExchange

from app.services.user_service.domain.entities import User
from app.services.user_service.domain.exceptions import (
    EmailAlreadyExists,
    UsernameAlreadyExists,
)
from app.services.user_service.infrastructure.db.models import User as UserModel
from app.services.user_service.infrastructure.messaging.events import UserCreated

if TYPE_CHECKING:
    from faststream.rabbit import RabbitBroker

    from app.services.user_service.domain.commands import CreateUserCommand
    from app.services.user_service.infrastructure.db.repositories import UserRepository
    from app.services.user_service.infrastructure.db.uow import UnitOfWork


USER_EVENTS_EX = RabbitExchange("user.events", type=ExchangeType.TOPIC, durable=True)


class CreateUserUseCase:
    def __init__(
        self,
        uow: "UnitOfWork",
        repo: "UserRepository",
        broker: "RabbitBroker",
    ) -> None:
        self.uow = uow
        self.repo = repo
        self.broker = broker

    async def execute(self, cmd: "CreateUserCommand") -> UserModel:
        async with self.uow:
            existing = await self.repo.get_by_email(cmd.email)
            if existing:
                raise EmailAlreadyExists(email=cmd.email)

            existing = await self.repo.get_by_username(cmd.username)
            if existing:
                raise UsernameAlreadyExists(username=cmd.username)

            user = User(
                username=cmd.username,
                first_name=cmd.first_name,
                last_name=cmd.last_name,
                email=cmd.email,
                phone_number=cmd.phone_number,
                wallet=cmd.wallet,
            )

            model = await self.repo.add(user)
            await self.uow.session.flush()

            event = UserCreated(
                user_id=user.id,
                username=user.username,
                email=user.email,
                phone_number=user.phone_number,
                occurred_at=datetime.now(UTC),
                correlation_id=str(uuid4()),
            )
            await self.broker.publish(
                event.model_dump(),
                exchange=USER_EVENTS_EX,
                routing_key="user.created",
            )

            return model
