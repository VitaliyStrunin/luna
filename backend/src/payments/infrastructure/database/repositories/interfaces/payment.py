from abc import ABC, abstractmethod


class IPaymentRepository(ABC):
    @abstractmethod
    async def create(self):
        pass
    
    @abstractmethod
    async def get_by_id(self):
        pass
    
    @abstractmethod
    async def get_by_idempotency_key(self):
        pass
    