from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from faststream.rabbit import RabbitBroker

from app.services.user_service.api.v1.routes import router as users_router
from app.services.user_service.infrastructure.ioc.containers import get_container

DOC = """
# User Service

Manage users (registration, profiles).
Publishes domain events to RabbitMQ (`user.created`).
"""


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    container: AsyncContainer = get_container()
    broker = await container.get(RabbitBroker)
    await broker.connect()
    yield
    await broker.stop()
    await container.close()


def create_app() -> FastAPI:
    application = FastAPI(
        title="User Service",
        version="1.0.0",
        summary="Services for working with users",
        description=DOC,
        lifespan=lifespan,
    )

    container = get_container()
    setup_dishka(container, application)
    application.include_router(users_router)
    return application


app = create_app()


if __name__ == "__main__":
    uvicorn.run("app.services.user_service.main:app", host="127.0.0.1", port=8000, reload=True)
# TODO: сделать доп провайдеры для создания настроек для Алхимии и фастапи.
# TODO: сделать тесты
# TODO: добавить Rate Limiting в FastAPI (например как ключ в редисе)
# TODO: добавить в ответ с регистраци api_key, либо возвратить только его в запросе
