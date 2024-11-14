import asyncio
import os
import httpx
import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from main import app
from src.database.models import Base, User
from src.database.db import get_db
from src.services.auth import auth_service

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create an asynchronous session
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

test_user = {
    "username": "markus",
    "email": "markus@example.com",
    "password": "12345678",
    "business_name": "FOP Markus"
}


@pytest_asyncio.fixture(scope="module", autouse=True)
async def session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = TestingSessionLocal()
    try:
        yield async_session
    finally:
        await async_session.close()


@pytest_asyncio.fixture(scope="module")
async def client(session):
    async def override_get_db():
        try:
            yield session
        finally:
            await session.close()

    app.dependency_overrides[get_db] = override_get_db

    async with httpx.AsyncClient(app=app, base_url="http://testserver") as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="module")
def user():
    return {
        "username": "markus",
        "email": "markus@example.com",
        "password": "12345678",
        "business_name": "FOP Markus"
    }


@pytest_asyncio.fixture(scope="module")
def check_object():
    return {
        "payment": {
            "amount": 896611.5,
            "type": "cash"
        },
        "products": [
            {
                "name": "Mavic 3T",
                "price": 298870.5,
                "quantity": 3
            }
        ]
    }


@pytest_asyncio.fixture()
async def token(client, user):
    await client.post("/api/auth/signup", json=user)
    response = await client.post(
        "/api/auth/login",
        json={"email": user.get("email"), "password": user.get("password")},
    )
    data = response.json()
    return data["access_token"]


@pytest.fixture(scope="module")
def event_loop():
    """
    Create a new event loop for the test session to avoid loop closure issues.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()
