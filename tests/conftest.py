import pytest
from httpx import AsyncClient
from app.main import app  # Import your FastAPI app

@pytest.fixture
async def async_client():


    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client