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
    