from fastapi import APIRouter, Depends
from app.services.merchant_service import MerchantService
from app.schemas.merchant import MerchantCreate
from app.core.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.auth.utils import generate_password_hash

merchants_router = APIRouter()
merchant_service = MerchantService()


@merchants_router.post("/register")
async def register(
    merchant_data: MerchantCreate, session: AsyncSession = Depends(get_session)
):
    merchant_data.password = generate_password_hash(merchant_data.password)
    merchant = await merchant_service.register(
        merchant_data=merchant_data, session=session
    )

    return merchant
