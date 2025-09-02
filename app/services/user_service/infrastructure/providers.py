from dishka import Provider, Scope, provide
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service.domain.use_cases import CreateUserUseCase
from app.services.user_service.infrastructure.db.repositories import UserRepository
from app.services.user_service.infrastructure.db.uow import UnitOfWork


class UserServiceProvider(Provider):
    def __init__(self) -> None:
        super().__init__(scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def uow(self, session: AsyncSession) -> UnitOfWork:
        print(session)
        return UnitOfWork(session)

    @provide(scope=Scope.REQUEST)
    def user_repo(self, session: AsyncSession) -> UserRepository:
        print(session)
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def create_user_uc(
        self,
        uow: UnitOfWork,
        user_repo: UserRepository,
        broker: RabbitBroker,
    ) -> CreateUserUseCase:
        return CreateUserUseCase(uow=uow, repo=user_repo, broker=broker)
