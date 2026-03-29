from faststream.rabbit import RabbitBroker

def create_broker(broker_url: str) -> RabbitBroker:
    return RabbitBroker(broker_url)
