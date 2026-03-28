from interfaces.payment import IPaymentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.payment import PaymentCreate, Payment
from database.models import PaymentDB

class PaymentRepositoryPostgres(IPaymentRepository):
    def __init__(self, session: AsyncSession):
        self.__session = session
    
    async def create_payment(self, create_schema: PaymentCreate) -> Payment:
        payment = PaymentDB(**create_schema.model_dump())