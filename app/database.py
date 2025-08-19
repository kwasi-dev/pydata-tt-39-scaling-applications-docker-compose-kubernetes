from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from .settings import get_settings


engine = create_async_engine(
    get_settings().database_url,
    echo=get_settings().debug,
    execution_options={"compiled_cache_size": 0},
    pool_size=get_settings().pool_size,
    max_overflow=get_settings().max_overflow,
    pool_timeout=get_settings().pool_timeout,
    pool_recycle=get_settings().pool_recycle,
    future=True)

async_session_maker = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=True
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session