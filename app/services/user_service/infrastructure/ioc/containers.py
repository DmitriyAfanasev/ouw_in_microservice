from functools import lru_cache

from dishka import make_async_container
from dishka.async_container import AsyncContainer

from app.core.settings import settings
from app.services.user_service.infrastructure.ioc.providers import (
    RabbitProvider,
    SqlAlchemyAsyncSessionDBProvider,
    SqlAlchemyPostgresDatabaseProvider,
    UserServiceProvider,
)


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(
        SqlAlchemyPostgresDatabaseProvider(dsn=settings.user_pg.user_db_dsn, echo=settings.SQL_ECHO),
        SqlAlchemyAsyncSessionDBProvider(),
        UserServiceProvider(),
        RabbitProvider(url=settings.rabbit.rabbitmq_url),
    )
