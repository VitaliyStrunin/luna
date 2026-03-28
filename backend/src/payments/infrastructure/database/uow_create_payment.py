from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.payments import PaymentRepositoryPostgres
from database.repositories.outbox import OutboxRepositoryPostgres


class UnitOfWorkPostgres:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def __aenter__(self):
        self.payment_repo = PaymentRepositoryPostgres(self.__session)
        self.outbox_repo = OutboxRepositoryPostgres(self.__session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.__session.rollback()
        else:
            await self.__session.commit()
