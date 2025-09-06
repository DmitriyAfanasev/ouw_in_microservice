from typing import Any

from faststream.rabbit import RabbitBroker

from app.services.user_service.domain.ports import EventPublisherProtocol


class RabbitEventPublisher(EventPublisherProtocol):
    def __init__(self, broker: RabbitBroker) -> None:
        self.broker = broker

    async def publish(self, event: dict[str, Any], routing_key: str) -> None:
        """
        Публикует событие в указанную очередь/обменник

        :param event: Данные события (словарь)
        :param routing_key: Ключ маршрутизации (например, 'user.created')
        """
        await self.broker.publish(
            message=event,
            routing_key=routing_key,
        )
