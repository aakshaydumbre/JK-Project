import pytest
from httpx import AsyncClient
from intelligent_book_manager.app.main import app

@pytest.mark.asyncio
async def test_create_book(async_client: AsyncClient):
    response = await async_client.post(
        "/books",
        json={
            "title": "Test Book",
            "author": "Author Name",
            "genre": "Fiction",
            "year_published": 2021,
            "summary": "A short summary."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Author Name"
    assert data["genre"] == "Fiction"
    assert data["year_published"] == 2021
    assert "id" in data

@pytest.mark.asyncio
async def test_get_books(async_client: AsyncClient):
    response = await async_client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "title" in data[0]
        assert "author" in data[0]
        assert "genre" in data[0]

@pytest.mark.asyncio
async def test_get_book_by_id(async_client: AsyncClient):
    book_id = 1  # Assuming a valid book ID
    response = await async_client.get(f"/books/{book_id}")
    assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_update_book(async_client: AsyncClient):
    book_id = 1
    response = await async_client.put(
        f"/books/{book_id}",
        json={
            "title": "Updated Title",
            "author": "New Author",
            "genre": "Non-Fiction",
            "year_published": 2022,
            "summary": "Updated summary"
        }
    )
    assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_delete_book(async_client: AsyncClient):
    book_id = 1
    response = await async_client.delete(f"/books/{book_id}")
    assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_add_review(async_client: AsyncClient):
    book_id = 1
    response = await async_client.post(
        f"/books/{book_id}/reviews",
        json={
            "user_id": "user123",
            "review_text": "Great book!",
            "rating": 5.0
        }
    )
    assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_get_reviews(async_client: AsyncClient):
    book_id = 1
    response = await async_client.get(f"/books/{book_id}/reviews")
    assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_get_summary(async_client: AsyncClient):
    book_id = 1
    response = await async_client.get(f"/books/{book_id}/summary")
    assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_get_recommendations(async_client: AsyncClient):
    response = await async_client.get("/recommendations")
    assert response.status_code == 200
