import pytest
import asyncio
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from intelligent_book_manager.app.database import get_db
from intelligent_book_manager.app.main import app
from httpx import AsyncClient, ASGITransport
from sqlalchemy.sql.selectable import Select  # ✅ Correct type for Select
from intelligent_book_manager.app.models.models import Book
from sqlalchemy import select

@pytest.fixture
def mock_db_session():
    """Fixture to create a properly mocked async database session."""
    session = AsyncMock(spec=AsyncSession)

    # ✅ Corrected async mock function for `execute()`
    async def mock_execute(query):
        mock_result = AsyncMock()
        if isinstance(query, Select):  # ✅ Proper check for Select type
            mock_scalars = AsyncMock()
            mock_scalars.all = AsyncMock(return_value=[
                Book(id=1, title="Mocked Book", author="Test Author", genre="Fantasy", year_published=2025, summary="Mocked Summary")
            ])  # ✅ Mocked book data
            mock_result.scalars = AsyncMock(return_value=mock_scalars)  # ✅ Ensure scalars() is awaitable
        return mock_result

    session.execute.side_effect = mock_execute  # ✅ Ensure execute() is awaitable
    return session

# ✅ Override FastAPI dependency injection with the mocked session
@pytest.fixture(autouse=True)
def override_dependency(mock_db_session):
    """Override FastAPI dependency injection to use the mock session."""
    app.dependency_overrides[get_db] = lambda: mock_db_session
    yield
    app.dependency_overrides.clear()  # ✅ Cleanup after each test

# ✅ Mocked async HTTP client for making requests
@pytest.fixture(scope="function")
async def async_client():
    """Fixture for async HTTP client using FastAPI app with mocked DB."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

# ✅ Proper event loop fixture to handle async tests
@pytest.fixture(scope="session")
def event_loop():
    """Ensure consistent event loop across all async tests."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()