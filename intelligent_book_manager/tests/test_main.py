import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from intelligent_book_manager.app.main import app  # Assuming your FastAPI app is in main.py
from intelligent_book_manager.app.models import models
from intelligent_book_manager.app.database import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Create a TestClient instance
client = TestClient(app)

# Setup Database for testing
models.Base.metadata.create_all(bind=engine)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[override_get_db] = override_get_db

class TestBookEndpoints(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()
        self.db.query(models.Book).delete()  # Clean up any existing data
        self.db.query(models.Review).delete()
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_create_book(self):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "genre": "Test Genre",
            "year_published": 2023,
        }
        response = client.post("/books", json=book_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Test Book")
        self.assertIsNotNone(response.json()["id"])

    def test_create_book_integrity_error(self):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "genre": "Test Genre",
            "year_published": 2023,
        }
        response = client.post("/books", json=book_data)
        self.assertEqual(response.status_code, 200)
        response = client.post("/books", json=book_data)
        self.assertEqual(response.status_code, 400) # duplicate title

    def test_get_books(self):
        book_data = {
            "title": "Test Book2",
            "author": "Test Author",
            "genre": "Test Genre",
            "year_published": 2023,
        }
        client.post("/books", json=book_data)
        response = client.get("/books")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

    def test_get_book(self):
        book_data = {
            "title": "Test Book3",
            "author": "Test Author",
            "genre": "Test Genre",
            "year_published": 2023,
        }
        created_book = client.post("/books", json=book_data).json()
        response = client.get(f"/books/{created_book['id']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Test Book3")

    def test_update_book(self):
        book_data = {
            "title": "Test Book4",
            "author": "Test Author",
            "genre": "Test Genre",
            "year_published": 2023,
        }
        created_book = client.post("/books", json=book_data).json()
        updated_book_data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "genre": "Updated Genre",
            "year_published": 2024,
        }
        response = client.put(f"/books/{created_book['id']}", json=updated_book_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated Book")

    def test_delete_book(self):
        book_data = {
            "title": "Test Book5",
            "author": "Test Author",
            "genre": "Test Genre",
            "year_published": 2023,
        }
        created_book = client.post("/books", json=book_data).json()
        response = client.delete(f"/books/{created_book['id']}")
        self.assertEqual(response.status_code, 200)
        response = client.get(f"/books/{created_book['id']}")
        self.assertEqual(response.status_code, 404)

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.db:Session = SessionLocal()
        self.db.query(models.Book).delete()  # Clean up any existing data
        self.db.query(models.Review).delete()
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "genre": "Test Genre",
            "year_published": 2023,
        }
        self.created_book = client.post("/books", json=book_data).json()
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_create_review(self):
        review_data = {
            "user_id": 1,
            "review_text": "Great book!",
            "rating": 4.5,
        }
        response = client.post(f"/books/{self.created_book['id']}/reviews", json=review_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["review_text"], "Great book!")

    def test_get_reviews(self):
        review_data = {
            "user_id": 1,
            "review_text": "Great book!",
            "rating": 4.5,
        }
        client.post(f"/books/{self.created_book['id']}/reviews", json=review_data)
        response = client.get(f"/books/{self.created_book['id']}/reviews")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

class TestSummaryAndRecommendations(unittest.TestCase):
    def setUp(self):
        self.db:Session = SessionLocal()
        self.db.query(models.Book).delete()  # Clean up any existing data
        self.db.query(models.Review).delete()
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "genre": "Test Genre",
            "year_published": 2023,
        }
        self.created_book = client.post("/books", json=book_data).json()
        self.db.commit()

    def tearDown(self):
        self.db.close()

    @patch("app.services.llama3_service.generate_summary") # Assuming this is the function that calls the external model
    def test_get_summary(self, mock_generate_summary):
        mock_generate_summary.return_value = "This is a test summary."
        response = client.get(f"/books/{self.created_book['id']}/summary")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["summary"], "This is a test summary.")

    def test_get_recommendations(self):
        book_data = {
            "title": "Test Book2",
            "author": "Test Author",
            "genre": "Science Fiction",
            "year_published": 2023,
        }
        client.post("/books", json=book_data).json()
        response = client.get("/recommendations?genre=Science Fiction")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) > 0)

if __name__ == "__main__":
    unittest.main()