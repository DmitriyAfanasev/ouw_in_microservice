from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class SqlAlchemyPostgresDatabaseProvider(Provider):
    def __init__(self, dsn: str, echo: bool = False) -> None:
        super().__init__(scope=Scope.APP)
        self._dsn = dsn
        self._echo = echo

    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(self._dsn, echo=self._echo, pool_pre_ping=True)
        try:
            yield engine
        finally:
            await engine.dispose()

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


class SqlAlchemyAsyncSessionDBProvider(Provider):
    def __init__(self) -> None:
        super().__init__(scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def session(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AsyncSession]:
        session = session_factory()
        try:
            yield session
        finally:
            await session.close()
