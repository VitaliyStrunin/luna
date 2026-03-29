import asyncio
import random

from src.worker.retry import retry_with_backoff
from src.worker.webhook import send_webhook
from src.worker.broker import get_broker
from src.payments.infrastructure.database.repositories.payments import PaymentRepositoryPostgres
from src.payments.infrastructure.database.repositories.outbox import OutboxRepositoryPostgres

from src.payments.infrastructure.dependencies import get_payment_repository
from src.payments.domain.entities.payment import PaymentStatus
from src.database.session import async_session_maker



broker = get_broker()

@broker.subscriber("payments.new")
async def process_payment(message: dict):
    async with async_session_maker() as session:
        idempotency_key = message['idempotency_key']
        
        payment_repo = PaymentRepositoryPostgres(session)
        outbox_repo = OutboxRepositoryPostgres(session)
        
        payment = await payment_repo.get_by_idempotency_key(idempotency_key)
        
        if not payment:
            print(f"No payment with {idempotency_key}")
            return
        
        if payment.status in (PaymentStatus.SUCCEEDED, PaymentStatus.FAILED):
            print(f"Payment already processed {idempotency_key}")
            return
        
        print(f"Processing payment {payment.id}")
        
        await asyncio.sleep(random.randint(2, 5))
        success = random.random() < 0.9
        status = PaymentStatus.SUCCEEDED if success else PaymentStatus.FAILED
        
        updated = await payment_repo.change_processing_status(idempotency_key, status)
        if not updated:
            print(f"Failed to update payment status")
            return
        
        updated_payment = await payment_repo.get_by_idempotency_key(idempotency_key)
        
        webhook_payload = {
            "payment_id": str(updated_payment.id),
            "status": updated_payment.status,
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
            
            outbox_events = await outbox_repo.get_unprocessed(limit=1)
            for event in outbox_events:
                if event.idempotency_key == idempotency_key:
                    await outbox_repo.mark_as_sent(event)
                    await session.commit()
                    
        except Exception as e:
            print(f"Failed to send webhook: {e}")