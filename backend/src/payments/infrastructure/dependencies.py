from src.database.session import get_async_db_session
from src.payments.infrastructure.database.units.uow_payment import UnitOfWorkPostgres
from src.payments.infrastructure.database.repositories.payments import PaymentRepositoryPostgres
from src.payments.application.use_cases.get_payment import GetPaymentUseCase
from src.payments.application.use_cases.create_payment import CreatePaymentUseCase
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

def get_payment_repository(session: AsyncSession = Depends(get_async_db_session)):
    return PaymentRepositoryPostgres(session)

def __get_unit_of_work(session: AsyncSession = Depends(get_async_db_session)):
    return UnitOfWorkPostgres(session)

def get_payment_use_case(payment_repo: PaymentRepositoryPostgres = Depends(get_payment_repository)):
    return GetPaymentUseCase(payment_repo)

def get_create_payment_use_case(uow: UnitOfWorkPostgres = Depends(__get_unit_of_work)):
    return CreatePaymentUseCase(uow)