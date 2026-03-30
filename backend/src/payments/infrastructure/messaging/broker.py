from faststream.rabbit import RabbitBroker, RabbitExchange
from src.core.config import settings


broker = RabbitBroker(settings.rabbitmq_url)

payment_exchange = RabbitExchange(
    name="payment_exchange",
    durable=True
)