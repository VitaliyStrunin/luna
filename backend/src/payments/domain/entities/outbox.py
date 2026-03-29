import uuid
from pydantic import BaseModel, ConfigDict
from typing import Any


class PaymentOutbox(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    idempotency_key: str
    payload: dict[str, Any]
    sent: bool = False
    
    
class PaymentOutboxCreate(BaseModel):
    idempotency_key: str
    payload: dict[str, Any]
    sent: bool = False
    
    
class PaymentOutboxUpdate(BaseModel):
    idempotency_key: str | None = None
    payload: dict[str, Any] | None = None
    sent: bool | None 