from app.models.api_key import ApiKey
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
import uuid
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status


class ApiKeyService:

    async def create_api_key(
        self, api_key_hash: str, merchant_id: uuid.UUID, session: AsyncSession
    ):

        api_key = await self.get_api_key_hash(merchant_id=merchant_id, session=session)

        if api_key:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already generated a key"
            )

        new_api_key_hash = ApiKey(api_key_hash=api_key_hash, merchant_id=merchant_id)

        try:

            session.add(new_api_key_hash)
            await session.commit()
            return

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="something went wrong"
            )

    async def get_api_key_hash(
        self,
        session: AsyncSession,
        hash: str = None,
        merchant_id: uuid.UUID = None,
    ):
        """
        Docstring for get_api_key_hash

        :param session: Description
        :type session: AsyncSession
        :param hash: Description
        :type hash: str
        :param merchant_id: Description
        :type merchant_id: uuid.UUID

        can be used to recover the key has
        """

        if merchant_id:

            statement = select(ApiKey).where(ApiKey.merchant_id == merchant_id)

        elif hash:
            statement = select(ApiKey).where(ApiKey.api_key_hash == hash)

        result = await session.execute(statement)
        return result.scalar_one_or_none()
