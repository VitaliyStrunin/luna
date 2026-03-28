from fastapi import APIRouter, Depends, Header, status
from src.payments.application.use_cases.get_payment import GetPaymentUseCase
from src.payments.application.use_cases.create_payment import CreatePaymentUseCase

from src.payments.infrastructure.dependencies import get_payment_use_case, get_create_payment_use_case
from src.payments.presentation.schemas.payments import PaymentConfirmCreateSchema, PaymentCreateSchema, PaymentReadSchema


payment_router = APIRouter(prefix="/api/v1")

@payment_router.get("/payments/{payment_id}",
                    response_model=PaymentReadSchema,
                    )
async def get_payment_info(
    payment_id: str,
    get_payment_use_case: GetPaymentUseCase = Depends(get_payment_use_case)
):
    pass


@payment_router.post("/payments",
                     response_model=PaymentConfirmCreateSchema, 
                     status_code=status.HTTP_202_ACCEPTED
                     )
async def create_payment(
    payment_info: PaymentCreateSchema, 
    create_payment_use_case: CreatePaymentUseCase = Depends(get_create_payment_use_case),
    idempotency_key: str = Header(alias="Idempotency-Key")
):
    pass