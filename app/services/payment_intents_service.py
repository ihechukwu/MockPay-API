import uuid
from fastapi import HTTPException, status
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.core.database import get_session
from app.models.payment_intent import PaymentIntent
from sqlalchemy import select


class PaymentIntentService:

    async def create_payment_intent(
        self, amount: float, merchant_id: uuid.UUID, session: AsyncSession
    ):

        reference = f"pay_{uuid.uuid4().hex[:12]}"
        intent = await self.get_payment_intent(reference=reference, session=session)
        if intent:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="payment intent already exists",
            )

        new_intent = PaymentIntent(
            amount=amount, merchant_id=merchant_id, reference=reference
        )

        try:
            session.add(new_intent)
            session.commit()

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="payment already exists"
            )

        return new_intent

    async def get_payment_intent(self, reference: uuid.UUID, session: AsyncSession):
        statement = select(PaymentIntent).where(PaymentIntent.reference == reference)
        result = await session.execute(statement)
        return result.scalar_one_or_none()
