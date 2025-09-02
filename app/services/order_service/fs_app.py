from datetime import datetime

from faststream import FastStream, Logger
from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange, RabbitQueue
from pydantic import BaseModel

broker = RabbitBroker("amqp://developer:password@localhost:5672/")

USER_EVENTS_EX = RabbitExchange(
    "user.events",
    type=ExchangeType.TOPIC,  # или ExchangeType.DIRECT, если без wildcard
    durable=True,
)
USER_CREATED_Q = RabbitQueue(
    "user.events.mailer",  # имя очереди
    durable=True,
    routing_key="user.created",  # ключ биндинга
)
app = FastStream(broker)


class UserIsRegister(BaseModel):
    username: str
    email: str
    phone_number: str
    occurred_at: datetime
    correlation_id: str


@broker.subscriber(USER_CREATED_Q, exchange=USER_EVENTS_EX)
async def new_user(user_data: UserIsRegister, logger: Logger) -> None:
    """Get new user from the broker"""
    logger.info("New user: %s", user_data)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info("Mail sent in %s", current_time)


if __name__ == "__main__":
    app.run()
