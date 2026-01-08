from pydantic import EmailStr
from typing import Optional
from sqlalchemy import table
from sqlmodel import Relationship, SQLModel, Field
import uuid
from datetime import datetime
from . import payment_intent
from typing import List


class Merchant(SQLModel, table=True):

    __tablename__ = "merchants"
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, unique=True
    )
    first_name: str = Field(max_length=50, min_length=1)
    last_name: str = Field(max_length=50, min_length=1)
    email: EmailStr = Field(unique=True, index=True)

    payment_intents: List["payment_intent.PaymentIntent"] = Relationship(
        back_populates="merchant",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    password: str = Field(exclude=True)
    is_verified: bool = Field(default=False)
    role: str = Field(default="user")
    created_at: datetime = Field(default_factory=datetime.utcnow)
