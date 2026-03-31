from src.core.exceptions import PaymentAlreadyExists
from src.payments.domain.entities.payment import Payment, PaymentCreate
from src.payments.infrastructure.database.units.uow_payment import UnitOfWorkPostgres


class CreatePaymentUseCase:
    def __init__(self, uow: UnitOfWorkPostgres):
        self.__uow = uow
    
    async def create_payment(self, payment_create: PaymentCreate) -> Payment:
        async with self.__uow as uow:
            existing_payment = await uow.payment_repo.get_by_idempotency_key(payment_create.idempotency_key)
            if existing_payment:
                raise PaymentAlreadyExists(payment_create.idempotency_key)

            payment = await uow.payment_repo.create(payment_create)
            payload = {
                "data": {
                    "payment_id": str(payment.id),
                    "created_at": payment.created_at.isoformat(),
                    "idempotency_key": payment_create.idempotency_key
                }
            }
            await uow.outbox_repo.create(
                payload,
                payment_create.idempotency_key
            )
            print(f"Created payment ID: {payment.id}, idempotency_key: {payment_create.idempotency_key}")

            return payment