from tkinter import CASCADE
from sqlalchemy import ForeignKey, table
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid
from typing import Optional


class ApiKey(SQLModel, table=True):

    __tablename__ = "api_keys"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, primary_key=True)
    merchant_id: uuid.UUID = ForeignKey("merchants.id", ondelete=CASCADE)
    api_key_hash: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_used_at: Optional[datetime]
