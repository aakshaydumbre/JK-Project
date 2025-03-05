import pytest
from httpx import AsyncClient
from intelligent_book_manager.app.main import app  # Ensure this is the correct import for your FastAPI app

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client