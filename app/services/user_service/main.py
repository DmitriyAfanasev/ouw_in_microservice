from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.settings import settings
from app.services.user_service.api.v1.routes import router as users_router
from app.services.user_service.infrastructure.db.providers import (
    PGDatabaseProvider,
    RequestDBProvider,
)
from app.services.user_service.infrastructure.messaging.providers import (
    MessagingProvider,
)
from app.services.user_service.infrastructure.providers import UserServiceProvider

DOC = """
# User Service

Manage users (registration, profiles).
Publishes domain events to RabbitMQ (`user.created`).
"""


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    engine = create_async_engine(settings.user_pg.user_db_dsn, echo=settings.SQL_ECHO)
    async with engine.begin() as conn:
        from app.services.user_service.infrastructure.db.models import Base

        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    application = FastAPI(
        title="User Service",
        version="1.0.0",
        summary="Services for working with users",
        description=DOC,
        lifespan=lifespan,
    )

    container = make_async_container(
        PGDatabaseProvider(dsn=settings.user_pg.user_db_dsn, echo=settings.SQL_ECHO),
        RequestDBProvider(),
        MessagingProvider(url=settings.rabbit.rabbitmq_url),
        UserServiceProvider(),
    )

    setup_dishka(container, application)
    application.include_router(users_router)
    return application


app = create_app()


if __name__ == "__main__":
    uvicorn.run("app.services.user_service.main:app", host="127.0.0.1", port=8000, reload=True)
