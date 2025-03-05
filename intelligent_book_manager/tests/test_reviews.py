import pytest
from unittest.mock import AsyncMock
from httpx import AsyncClient, ASGITransport
from intelligent_book_manager.app.main import app
from intelligent_book_manager.app.models.models import Review
from intelligent_book_manager.app.database import get_db

@pytest.fixture
def mock_db_session(mocker):
    session = AsyncMock(spec=AsyncSession)
    mocker.patch("intelligent_book_manager.app.database.get_db", return_value=session)
    return session

@pytest.mark.asyncio
async def test_add_review(mock_db_session):
    """Test adding a review to a book."""
    review_data = {
        "user_id": "user123",
        "review_text": "Amazing book!",
        "rating": 4.5
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/books/1/reviews", json=review_data)

    assert response.status_code == 200
    assert response.json() == {"message": "Review added successfully"}

@pytest.mark.asyncio
async def test_get_reviews(mock_db_session):
    """Test retrieving reviews for a book."""
    mock_reviews = [
        Review(id=1, book_id=1, user_id="user123", review_text="Great book!", rating=5),
        Review(id=2, book_id=1, user_id="user456", review_text="Not bad", rating=3.5)
    ]

    mock_db_session.execute.return_value.scalars.return_value.all.return_value = mock_reviews

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/books/1/reviews")

    assert response.status_code == 200
    assert len(response.json()) == 2