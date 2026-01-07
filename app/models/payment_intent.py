from tkinter import CASCADE
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
import uuid
from datetime import datetime


class PaymentIntent(SQLModel, table=True):

    __tablename__ = "payment_intents"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, unique=True, index=True
    )
    merchant_id: uuid.UUID = Field("merchants.id", nullable=False, index=True)
    merchant: "Merchant" = Relationship(back_populates="payment_intents")
    amount: int
    currency: str = Field(default="NGN", max_length=3)
    status: str = Field(default="requires_payment", index=True)
    reference: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )
    updated_at: datetime = None
