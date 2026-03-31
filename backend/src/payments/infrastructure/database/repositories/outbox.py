from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.payments.domain.entities.outbox import PaymentOutbox
from src.payments.infrastructure.database.models.outbox import PaymentOutboxDB
from src.payments.infrastructure.database.repositories.interfaces.outbox import (
    IOutboxRepository,
)


class OutboxRepositoryPostgres(IOutboxRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session
    
    async def create(self, payload: dict[str, Any], idempotency_key: str):
        outbox = PaymentOutboxDB(
            payload=payload,
            idempotency_key=idempotency_key
        )
        
        self.__session.add(outbox)
        await self.__session.flush()

    async def get_unprocessed(self, limit: int = 100) -> list[PaymentOutbox]:
        result = await self.__session.execute(
            select(PaymentOutboxDB)
            .where(PaymentOutboxDB.sent == False)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def mark_as_sent(self, idempotency_key: str):
        await self.__session.execute(
            update(PaymentOutboxDB)
            .where(PaymentOutboxDB.idempotency_key == idempotency_key)
            .values(sent=True)
        )
        await self.__session.flush()