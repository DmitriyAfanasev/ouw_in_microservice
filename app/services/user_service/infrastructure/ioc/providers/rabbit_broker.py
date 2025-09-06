from dishka import Provider, Scope, provide
from faststream.rabbit import RabbitBroker

from app.services.user_service.domain.ports import EventPublisherProtocol
from app.services.user_service.infrastructure.brokers.rabbit import RabbitEventPublisher


class RabbitProvider(Provider):
    def __init__(self, url: str) -> None:
        super().__init__(scope=Scope.APP)
        self._url = url

    @provide(scope=Scope.APP)
    async def get_broker(self) -> RabbitBroker:
        return RabbitBroker(self._url)

    @provide(scope=Scope.REQUEST)
    def get_event_publisher(self, broker: RabbitBroker) -> EventPublisherProtocol:
        return RabbitEventPublisher(broker)
