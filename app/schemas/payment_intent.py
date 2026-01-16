from pydantic import BaseModel


class PaymentIntentCreate(BaseModel):

    amount: float
