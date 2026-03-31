import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, HttpUrl


class Currency(str, Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class Payment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    amount: Decimal
    currency: Currency 
    description: str | None = None
    meta: dict[str, Any] | None = None
    status: PaymentStatus
    idempotency_key: str
    webhook_url: str 
    created_at: datetime
    processed_at: datetime | None = None


class PaymentCreate(BaseModel):
    amount: Decimal
    currency: Currency 
    description: str | None = None
    meta: dict[str, Any] | None = None
    webhook_url: str
    idempotency_key: str
    