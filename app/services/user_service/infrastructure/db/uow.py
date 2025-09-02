from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._txn: AsyncSessionTransaction | None = None

    async def __aenter__(self) -> "UnitOfWork":
        self._txn = await self.session.begin()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: type[BaseException] | None,
        tb: TracebackType | None,
    ) -> None:
        if exc:
            await self.session.rollback()
        else:
            await self.session.commit()
