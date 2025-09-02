from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from faststream.rabbit import RabbitBroker


class MessagingProvider(Provider):
    def __init__(self, url: str) -> None:
        super().__init__(scope=Scope.APP)
        self._url = url

    @provide(scope=Scope.APP)
    async def broker(self) -> AsyncIterator[RabbitBroker]:
        broker = RabbitBroker(self._url)
        await broker.start()
        try:
            yield broker
        finally:
            await broker.stop()
