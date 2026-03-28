
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.core.dependcies import get_async_db
from app.main import app as prod_app

from sqlalchemy.ext.asyncio import async_sessionmaker
from app.core.database import Base


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()

@pytest_asyncio.fixture(scope="session")
async def session_maker(test_engine):
    return async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session")
async def test_app(session_maker):
    async def _get_async_db():
        async with session_maker() as session:
            yield session

    prod_app.dependency_overrides[get_async_db] = _get_async_db
    yield prod_app
    prod_app.dependency_overrides.clear()

@pytest_asyncio.fixture(scope="session")
async def test_client(test_app: FastAPI):
    transport = ASGITransport(app=prod_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
