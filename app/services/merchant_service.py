from sqlalchemy import select
from pydantic import EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.merchant import Merchant
from app.schemas.merchant import MerchantCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status


class MerchantService:

    async def register(self, merchant_data: MerchantCreate, session: AsyncSession):

        new_merchant = Merchant(**merchant_data.model_dump())

        try:
            session.add(new_merchant)
            await session.commit()
            session.refresh(new_merchant)
            return new_merchant

        except IntegrityError:

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong",
            )

    async def get_merchant_by_email(self, email: EmailStr, session: AsyncSession):

        statement = select(Merchant).where(Merchant.email == email)
        result = await session.execute(statement)
        merchant = result.scalar_one_or_none()
        return merchant

    async def verify_merchant_by_email(self, email: EmailStr, session: AsyncSession):

        merchant = await self.get_merchant_by_email(email=email, session=session)

        if merchant.is_verified:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already verified "
            )

        merchant.is_verified = True
        await session.commit()
