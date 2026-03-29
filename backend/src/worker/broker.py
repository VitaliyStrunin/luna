from src.core.config import settings
from faststream.rabbit import RabbitBroker

def get_broker() -> RabbitBroker:
    return RabbitBroker(settings.rabbitmq_url)
