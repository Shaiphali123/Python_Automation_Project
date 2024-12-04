"""import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport  # Use ASGITransport for async testing
from app.main import app  # Import your FastAPI app


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as client:
        yield client"""



import pytest
from httpx import AsyncClient
from app.main import app  # Import your FastAPI app





@pytest.fixture
async def async_client():
    """
    Fixture to create an async HTTP client for integration tests.
    """
    # Directly create AsyncClient instance for testing
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client  # Yielding the actual AsyncClient instance, NOT an async generator.
