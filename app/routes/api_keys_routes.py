from app.core.security import generate_api_key, hash_api_key
from fastapi import Depends, APIRouter
from app.core.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.dependency import get_current_user
from app.services.api_keys_service import ApiKeyService

api_keys_routers = APIRouter()
api_key_service = ApiKeyService()


@api_keys_routers.get("/generate-api-key")
async def generate_key(
    merchant=Depends(get_current_user), session: AsyncSession = Depends(get_session)
):

    merchant_id = merchant.id
    raw_key = generate_api_key()
    key_hash = hash_api_key(raw_key)
    await api_key_service.create_api_key(
        api_key_hash=key_hash, merchant_id=merchant_id, session=session
    )

    return {"api_key": raw_key, "warning": "store this key securely"}
