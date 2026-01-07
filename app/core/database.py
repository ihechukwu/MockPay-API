from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = AsyncEngine(create_engine(url=settings.DATABASE_URL))


async def get_session():
    Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    async with Session() as session:
        yield session
