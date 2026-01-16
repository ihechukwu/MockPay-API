import uuid
from app.core.dependencies import api_key_auth
from fastapi import APIRouter, Depends
from app.core.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.payment_intents_service import PaymentIntentService
from app.schemas.payment_intent import PaymentIntentCreate


payments_router = APIRouter()
payment_intent_service = PaymentIntentService()


@payments_router.post("/create-intent")
async def create_payment_intent(
    payment_data: PaymentIntentCreate,
    merchant_id: uuid.UUID = Depends(api_key_auth),
    session: AsyncSession = Depends(get_session),
):

    intent = await payment_intent_service.create_payment_intent(
        amount=payment_data.amount, merchant_id=merchant_id, session=session
    )

    return {
        "amount": intent.amount,
        "reference": intent.reference,
        "status": intent.status,
    }
