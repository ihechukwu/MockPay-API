from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.merchant import MerchantLogin
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.merchant_service import MerchantService
from app.core.database import get_session
from .utils import create_access_token, verify_password_hash
from datetime import timedelta
from app.core.config import settings


auths_router = APIRouter()
merchant_service = MerchantService()


@auths_router.post("/login")
async def login(
    merchant_data: MerchantLogin, session: AsyncSession = Depends(get_session)
):
    merchant_email = merchant_data.email
    merchant = await merchant_service.get_merchant_by_email(
        merchant_email, session=session
    )
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="merchant not found"
        )

    password_valid = verify_password_hash(merchant_data.password, merchant.password)
    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    payload = {"merchant_email": merchant_email, "merchant_id": str(merchant.id)}
    access_token = create_access_token(payload)
    refresh_token = create_access_token(
        payload,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        refresh=True,
    )

    return {"Access Token": access_token, "Refresh Token": refresh_token}
