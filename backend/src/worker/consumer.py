import asyncio
import logging
import random

from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue
from src.core.config import settings
from src.database.session import async_session_maker
from src.payments.domain.entities.payment import PaymentStatus
from src.payments.infrastructure.database.units.uow_payment import UnitOfWorkPostgres
from src.worker.retry import retry_with_backoff
from src.worker.webhook import send_webhook

logger = logging.getLogger(__name__)

broker = RabbitBroker(settings.rabbitmq_url)

payment_exchange = RabbitExchange("payment_exchange", durable=True)
dlq_exchange = RabbitExchange("dlq_exchange", durable=True)

payment_queue = RabbitQueue(
    name="payments.new",
    routing_key="payment_new",
    durable=True,
    arguments={
        "x-dead-letter-exchange": "dlq_exchange",
        "x-dead-letter-routing-key": "dlq_queue",
    },
)

dlq_queue = RabbitQueue(
    name="dlq_queue",
    routing_key="dlq_queue",
    durable=True,
)

app = FastStream(broker)

@broker.subscriber(payment_queue, payment_exchange)
async def process_payment(message: dict):
    async with async_session_maker() as session:
        uow = UnitOfWorkPostgres(session)
        async with uow:
            message_data = message["data"]
            idempotency_key = message_data["idempotency_key"]

            payment = await uow.payment_repo.get_by_idempotency_key(idempotency_key)

            if not payment:
                logger.warning(f"Payment with idempotency_key={idempotency_key} not found")
                return

            if payment.status in (PaymentStatus.SUCCEEDED, PaymentStatus.FAILED):
                logger.info(f"Payment {payment.id} was already processed")
                return

            logger.info(f"Started processing payment {payment.id}")

            await asyncio.sleep(random.randint(2, 5))
            success = random.random() < 0.9
            status = PaymentStatus.SUCCEEDED if success else PaymentStatus.FAILED

            updated = await uow.payment_repo.change_processing_status(idempotency_key, status)
            if not updated:
                logger.error(f"Error while updating payment {payment.id} status")
                return

            updated_payment = await uow.payment_repo.get_by_idempotency_key(idempotency_key)

            webhook_payload = {
                "payment_id": str(updated_payment.id),
                "status": updated_payment.status.value,
                "idempotency_key": idempotency_key,
            }

            try:
                await retry_with_backoff(
                    send_webhook,
                    max_attempts=3,
                    base_delay=1.0,
                    webhook_url=updated_payment.webhook_url,
                    payload=webhook_payload,
                )

                logger.info(f"Webhook of payment {payment.id} sent")

                await uow.outbox_repo.mark_as_sent(
                    idempotency_key
                )

            except Exception as e:
                logger.error(f"Webhook error: {e}")
                raise e

@broker.subscriber(dlq_queue, dlq_exchange)
async def process_dlq(message: dict):
    logger.error(f"DLQ message: {message}")