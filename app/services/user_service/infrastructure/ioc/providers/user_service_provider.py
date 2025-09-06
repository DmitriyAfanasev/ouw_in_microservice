from dishka import Provider, Scope, provide
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service.domain.ports import (
    EventPublisherProtocol,
    UnitOfWorkProtocol,
    UserRepositoryProtocol,
)
from app.services.user_service.domain.use_cases import CreateUserUseCase
from app.services.user_service.infrastructure.brokers.rabbit import RabbitEventPublisher
from app.services.user_service.infrastructure.db.repositories import UserRepository
from app.services.user_service.infrastructure.db.uow import UnitOfWork


class UserServiceProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def uow(self, session: AsyncSession) -> UnitOfWorkProtocol:
        """Фабрика для создания UnitOfWork (Паттерн управления транзакциями)"""
        return UnitOfWork(session)

    @provide
    def user_repo(self, session: AsyncSession) -> UserRepositoryProtocol:
        """Фабрика для создания репозитория пользователей"""
        return UserRepository(session)

    @provide
    def event_publisher(self, publisher: RabbitBroker) -> EventPublisherProtocol:
        """Фабрика для создания брокера сообщений"""
        return RabbitEventPublisher(publisher)

    @provide
    def create_user_uc(
        self,
        uow: UnitOfWorkProtocol,
        user_repo: UserRepositoryProtocol,
        event_publisher: EventPublisherProtocol,
    ) -> CreateUserUseCase:
        """Фабрика для создания user_case создания пользователя"""
        return CreateUserUseCase(uow=uow, repo=user_repo, event_publisher=event_publisher)
