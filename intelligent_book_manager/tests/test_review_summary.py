import pytest
from unittest.mock import AsyncMock
from httpx import AsyncClient, ASGITransport
from intelligent_book_manager.app.main import app
from intelligent_book_manager.app.services.llama3_service import generate_review_summary

@pytest.fixture
def mock_generate_review_summary(mocker):
    mock_summary_function = AsyncMock()
    mock_summary_function.return_value = "This is a summarized review."
    mocker.patch("intelligent_book_manager.app.services.llama3_service.generate_review_summary", mock_summary_function)
    app.dependency_overrides[generate_review_summary] = mock_summary_function
    return mock_summary_function

@pytest.mark.asyncio
async def test_generate_review_summary(mock_generate_review_summary):
    """Test AI-generated review summary."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/generate-review-summary", json={"reviews": ["Great book!", "Very informative."]})

    assert response.status_code == 200
    assert response.json()["review_summary"] == "This is a summarized review."