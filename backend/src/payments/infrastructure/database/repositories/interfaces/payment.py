from abc import ABC, abstractmethod

from src.payments.domain.entities.payment import Payment, PaymentCreate, PaymentStatus


class IPaymentRepository(ABC):
    @abstractmethod
    async def create(self, payment_data: PaymentCreate) -> Payment:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Payment | None:
        pass
    
    @abstractmethod
    async def get_by_idempotency_key(self, idempotency_key: str) -> Payment | None:
        pass
    
    @abstractmethod
    async def change_processing_status(self, idempotency_key: str, status: PaymentStatus) -> bool:
        pass