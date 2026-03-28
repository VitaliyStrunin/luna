from database.session import get_async_db_session
from infrastructure.database.uow_create_payment import UnitOfWorkPostgres
from infrastructure.database.repositories.payments import PaymentRepositoryPostgres
from application.use_cases.get_payment import GetPaymentUseCase
from application.use_cases.create_payment import CreatePaymentUseCase


def __get_payment_repository():
    session = get_async_db_session()
    return PaymentRepositoryPostgres(session)

def __get_unit_of_work():
    session = get_async_db_session()
    return UnitOfWorkPostgres(session)

def get_payment_use_case():
    payment_repo = __get_payment_repository()
    return GetPaymentUseCase(payment_repo)

def get_create_payment_use_case():
    uow = __get_unit_of_work()
    return CreatePaymentUseCase(uow)