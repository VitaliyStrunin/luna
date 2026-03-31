import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field, HttpUrl
from src.payments.domain.entities.payment import Currency, PaymentStatus


class PaymentReadSchema(BaseModel):
    id: uuid.UUID
    amount: Decimal = Field(ge=0)
    currency: Currency 
    description: str | None = None
    meta: dict[str, Any] | None = None
    status: PaymentStatus
    idempotency_key: str
    webhook_url: HttpUrl 
    created_at: datetime
    processed_at: datetime | None = None


class PaymentCreateSchema(BaseModel):
    amount: Decimal = Field(ge=0)
    currency: Currency 
    description: str | None = None
    meta: dict[str, Any] | None = None
    webhook_url: HttpUrl
    

class PaymentConfirmCreateSchema(BaseModel):
    id: uuid.UUID
    status: PaymentStatus
    created_at: datetime
