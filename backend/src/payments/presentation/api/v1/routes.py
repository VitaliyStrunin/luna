from fastapi import APIRouter, Depends, Header, status, HTTPException
from src.payments.application.use_cases.get_payment import GetPaymentUseCase
from src.payments.application.use_cases.create_payment import CreatePaymentUseCase

from src.payments.infrastructure.dependencies import get_payment_use_case, get_create_payment_use_case
from src.payments.presentation.schemas.payments import PaymentConfirmCreateSchema, PaymentCreateSchema, PaymentReadSchema
from src.payments.domain.entities.payment import PaymentCreate
from src.core.security import verify_api_key
from src.core.exceptions import PaymentAlreadyExists, PaymentNotFoundByID


payment_router = APIRouter(prefix="/api/v1", dependencies=[Depends(verify_api_key)])


@payment_router.get("/payments/{payment_id}",
                    response_model=PaymentReadSchema,
                    )
async def get_payment_info_by_id(
    payment_id: str,
    get_payment_use_case: GetPaymentUseCase = Depends(get_payment_use_case)
):  
    try:
        payment = await get_payment_use_case.get_by_id(payment_id)
        return payment
    except PaymentNotFoundByID as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=e.message)

@payment_router.post("/payments",
                     response_model=PaymentConfirmCreateSchema, 
                     status_code=status.HTTP_202_ACCEPTED
                     )
async def create_payment(
    payment_data: PaymentCreateSchema, 
    create_payment_use_case: CreatePaymentUseCase = Depends(get_create_payment_use_case),
    idempotency_key: str = Header(alias="Idempotency-Key")
):
    try:
        payment_create = PaymentCreate(**payment_data.model_dump(mode="json"), idempotency_key=idempotency_key)
        payment = await create_payment_use_case.create_payment(payment_create)
        return payment
    except PaymentAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": e.message}
        )
