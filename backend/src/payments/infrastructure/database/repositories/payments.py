from src.payments.infrastructure.database.repositories.interfaces.payment import IPaymentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.payments.domain.entities.payment import PaymentCreate, Payment, PaymentStatus
from src.payments.infrastructure.database.models.payment import PaymentDB
from sqlalchemy import select, update


class PaymentRepositoryPostgres(IPaymentRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session
    
    async def create(self, payment_data: PaymentCreate) -> Payment:
        payment_db = PaymentDB(**payment_data.model_dump())
        self.__session.add(payment_db)
        await self.__session.flush()
        return Payment.model_validate(payment_db)
        
    async def get_by_id(self, id: str) -> Payment | None:
        payment = await self.__session.get(PaymentDB, id) 
        return Payment.model_validate(payment) if payment else None
    
    async def get_by_idempotency_key(self, idempotency_key: str) -> Payment | None:
        query =  select(PaymentDB).where(PaymentDB.idempotency_key == idempotency_key)
        result = await self.__session.execute(query)
        payment = result.scalar_one_or_none()
        return Payment.model_validate(payment) if payment else None
    
    async def change_processing_status(self, idempotency_key: str, status: PaymentStatus) -> bool:
        result = await self.__session.execute(
            update(PaymentDB)
            .where(
                PaymentDB.idempotency_key == idempotency_key,
                PaymentDB.status == PaymentStatus.PENDING,
            )
            .values(status=status)
        )
        await self.__session.commit()
        return result.rowcount > 0
