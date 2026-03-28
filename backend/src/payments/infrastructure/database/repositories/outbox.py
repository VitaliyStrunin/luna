from interfaces.outbox import IOutboxRepository
from sqlalchemy.ext.asyncio import AsyncSession

class OutboxRepositoryPostgres(IOutboxRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session