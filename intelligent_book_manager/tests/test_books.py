import app
import pytest
from httpx import ASGITransport
from intelligent_book_manager.app.main import app
from sqlalchemy.orm import declarative_base

# @pytest.mark.asyncio
# async def test_create_book(override_get_db):
#     """Test creating a book."""
#     import httpx  # Explicitly import httpx to avoid issues
#
#     async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
#         response = await client.post("/books", json={
#             "title": "Test Book",
#             "author": "Test Author",
#             "genre": "Fantasy",
#             "year_published": 2025,
#             "summary": "A test summary."
#         })
#     assert response.status_code == 200
#     assert response.json()["title"] == "Test Book"


@pytest.mark.asyncio
async def test_get_books(async_client):
    """Test retrieving all books."""
    response = await async_client.get("/books")
    assert response.status_code == 200
    # assert isinstance(response.json(), list)

#
# @pytest.mark.asyncio
# async def test_get_book_by_id(async_client):
#     """Test retrieving a book by ID."""
#     book_data = {
#         "title": "Mocked Book",
#         "author": "Mock Author",
#         "genre": "Fiction",
#         "year_published": 2021,
#         "summary": "Test summary"
#     }
#     create_response = await async_client.post("/books", json=book_data)
#     print("Create Response:", create_response.json())  # ✅ Debugging Step
#
#     assert create_response.status_code == 200  # Ensure book creation succeeds
#
#     book_id = create_response.json().get("id")  # Use `.get()` to avoid `KeyError`
#     assert book_id is not None, "Book ID was not returned in response"
#
#     response = await async_client.get(f"/books/{book_id}")
#     assert response.status_code == 200
#
#
# @pytest.mark.asyncio
# async def test_delete_book(async_client):
#     """Test deleting a book."""
#     book_data = {
#         "title": "Book to Delete",
#         "author": "Author",
#         "genre": "Mystery",
#         "year_published": 2015
#     }
#     create_response = await async_client.post("/books", json=book_data)
#     book_id = create_response.json()["id"]
#
#     delete_response = await async_client.delete(f"/books/{book_id}")
#
#     assert delete_response.status_code == 200
#     assert delete_response.json() == {"message": "Book deleted successfully"}
#
#     # Verify book is deleted
#     get_response = await async_client.get(f"/books/{book_id}")
#     assert get_response.status_code == 404