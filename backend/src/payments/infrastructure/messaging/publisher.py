import asyncio
import logging

from faststream.rabbit import RabbitBroker, RabbitExchange
from src.database.session import async_session_maker
from src.payments.infrastructure.database.repositories.outbox import (
    OutboxRepositoryPostgres,
)
from src.payments.infrastructure.messaging.broker import broker, payment_exchange

logger = logging.getLogger(__name__)

class OutboxPublisher:
    def __init__(
        self,
        session_maker,
        broker: RabbitBroker,
        exchange: RabbitExchange,
        routing_key: str,
    ):
        self.__session_maker = session_maker
        self.__broker = broker
        self.__exchange = exchange
        self.__routing_key = routing_key
        self.__running = True

    def stop(self):
        self.__running = False

    async def run(self):
        while self.__running:
            async with self.__session_maker() as session:
                repo = OutboxRepositoryPostgres(session)
                events = await repo.get_unprocessed(limit=100)
                if not events:
                    await asyncio.sleep(1)
                    continue
                logger.info(f"Found {len(events)} messages")
                for event in events:
                    try:
                        await self.__broker.publish(
                            message=event.payload,
                            exchange=self.__exchange,
                            routing_key=self.__routing_key,
                        )

                        await repo.mark_as_sent(event.idempotency_key)

                    except Exception as e:
                        logger.error(f"Something went wrong while sending message: {e}")

                await session.commit()

outbox_publisher = OutboxPublisher(
    session_maker=async_session_maker,
    broker = broker,
    exchange=payment_exchange,
    routing_key="payment_new"
)
