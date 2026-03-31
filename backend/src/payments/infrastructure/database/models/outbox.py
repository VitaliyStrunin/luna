import uuid
from typing import Any

from sqlalchemy import JSON, UUID, Boolean, String, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from src.database.base import Base


class PaymentOutboxDB(Base):
    __tablename__ = "payment_outbox"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, 
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    
    idempotency_key: Mapped[str] = mapped_column(
        String,
        unique=True, 
        index=True,
        nullable=False
    )
    
    payload: Mapped[dict[str, Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"), 
        nullable=False
    )
    
    sent: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False, 
        default=False
    )