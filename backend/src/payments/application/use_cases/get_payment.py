from src.core.exceptions import PaymentNotFoundByID, PaymentNotFoundByIdempotencyKey
from src.payments.domain.entities.payment import Payment
from src.payments.infrastructure.database.repositories.interfaces.payment import (
    IPaymentRepository,
)


class GetPaymentUseCase:
    def __init__(self, payment_repo: IPaymentRepository):
        self.__payment_repo = payment_repo
    
    async def get_by_id(self, payment_id: str) -> Payment:
        payment = await self.__payment_repo.get_by_id(payment_id)
        if payment is None:
            raise PaymentNotFoundByID(payment_id)
        return payment
    
    async def get_by_idempotency_key(self, idempotency_key: str) -> Payment:
        payment = await self.__payment_repo.get_by_idempotency_key(idempotency_key)
        if payment is None:
            raise PaymentNotFoundByIdempotencyKey(idempotency_key)
        return payment
    