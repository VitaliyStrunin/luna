import uuid
from decimal import Decimal
from datetime import datetime, timezone
from database.base import Base
from sqlalchemy import func, UUID, Numeric, String, Text, JSON, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Any
from domain.entities.payment import PaymentStatus, Currency

class PaymentDB(Base):
    __tablename__ = "payments"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID, 
        primary_key=True,
        default=uuid.uuid4
    )
    
    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )
    
    currency: Mapped[Currency] = mapped_column(
        Enum(Currency),
        nullable=False
    )
    
    description: Mapped[str|None] = mapped_column(
        Text,
        nullable=True
    )
    
    meta: Mapped[dict[str, Any]|None] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"), 
        nullable=True
    )
    
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False,
    )
    
    idempotency_key: Mapped[str] = mapped_column(
        String(256),
        nullable=False, 
        unique=True, 
        index=True
    )
    
    webhook_url: Mapped[str] = mapped_column(
        String(1024),
        nullable=False
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False, 
        index=True
    )
    
    processed_at: Mapped[datetime|None] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True
    )