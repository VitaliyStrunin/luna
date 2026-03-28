from infrastructure.database.uow_create_payment import UnitOfWorkPostgres
from domain.entities.payment import PaymentCreate, Payment

class CreatePaymentUseCase:
    def __init__(self, uow: UnitOfWorkPostgres):
        self.__uow = uow
    
    def create_payment(self, payment_create: PaymentCreate) -> Payment:
        with self.__uow as uow:
            ...