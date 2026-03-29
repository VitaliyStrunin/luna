from faststream.rabbit import RabbitBroker


class MessageProducer:
    def __init__(self, broker: RabbitBroker):
        self.__broker = broker
        
    async def publish(self, queue: str, message: dict):
        await self.__broker.publish(message, queue=queue)