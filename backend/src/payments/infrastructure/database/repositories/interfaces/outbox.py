from abc import ABC, abstractmethod
from typing import Any

from src.payments.domain.entities.outbox import PaymentOutbox


class IOutboxRepository(ABC):
    @abstractmethod
    async def create(self, payload: dict[str, Any], idempotency_key: str):
        pass

    @abstractmethod
    async def get_unprocessed(self, limit: int) -> list[PaymentOutbox]:
        pass
    
    @abstractmethod
    async def mark_as_sent(self, idempotency_key: str):
        pass