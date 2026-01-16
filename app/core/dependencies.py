from email.policy import HTTP
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Request, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services import merchant_service
from .database import get_session
from app.auth.utils import decode_access_token
from app.services.merchant_service import MerchantService
from app.services.api_keys_service import ApiKeyService
from app.core.security import hash_api_key
from datetime import datetime


merchant_service = MerchantService()
api_key_service = ApiKeyService()
bearer_scheme = HTTPBearer(auto_error=True)


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:

        cred = await super().__call__(request)
        token = cred.credentials
        payload = self.token_is_valid(token)
        self.verify_access_token(payload)
        return payload

    def token_is_valid(self, token: str):

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token"
            )
        payload = decode_access_token(token)
        return payload

    def verify_access_token(self, payload: dict):

        raise NotImplementedError("Please override this method in child class")


class AccessTokenBearer(TokenBearer):
    def verify_access_token(self, payload: dict):
        if payload and payload["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Provide access token"
            )


class RefreshTokenBearer(TokenBearer):
    def verify_access_token(self, payload: dict):
        if payload and not payload["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Provide refresh token"
            )


async def get_current_user(
    merchant: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    merchant_email = merchant.get("merchant_email")
    merchant = await merchant_service.get_merchant_by_email(merchant_email, session)

    return merchant


class RoleChecker:

    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, merchant=Depends(get_current_user)):
        if merchant.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Access Denied"
            )


async def api_key_auth(
    cred: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_session),
):

    raw_key = cred.credentials
    if not raw_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Key"
        )

    api_hashed_key = await api_key_service.get_api_key_hash(
        hash=hash_api_key(raw_key), session=session
    )

    if not api_hashed_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or revoked key"
        )

    api_hashed_key.last_used_at = datetime.utcnow()
    await session.commit()

    return api_hashed_key.merchant_id
