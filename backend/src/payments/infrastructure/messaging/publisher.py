import asyncio

from src.payments.infrastructure.messaging.producer import MessageProducer
from src.payments.infrastructure.database.repositories.outbox import OutboxRepositoryPostgres


class OutboxPublisher:
    def __init__(self, session_maker, producer: MessageProducer, queue: str):
        self.__session_maker = session_maker
        self.__producer = producer
        self.__running = True
        self.__queue = queue
    
    async def stop(self):
        self.__running = False
        
    async def run(self):
        while self.__running:
            async with self.__session_maker() as session:
                repo = OutboxRepositoryPostgres(session)
                events = await repo.get_unprocessed(limit=100)
                
                if not events:
                    await asyncio.sleep(1)
                    continue
                for event in events:
                    try:
                        await self.__producer.publish(
                            queue=self.__queue, 
                            message=event.payload
                        )
                        await repo.mark_as_sent(event)
                    except Exception as e:
                        pass # TODO
                await session.commit()
                