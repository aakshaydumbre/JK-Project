## Technologies Used

-   **FastAPI:** Modern, fast (high-performance) web framework for building APIs with Python.
-   **SQLAlchemy:** Python SQL toolkit and Object-Relational Mapping (ORM) system.
-   **PostgreSQL:** Open-source relational database management system.
-   **Asyncio & Asyncpg:** Asynchronous programming for efficient I/O operations.
-   **Pydantic:** Data validation and settings management using Python type annotations.
-   **Docker:** Containerization for simplified deployment and environment consistency.
-   **LLama3 (or other Large Language Model):** (If implemented) For generating book summaries.
- **python-dotenv:** manage the environment variables.

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/aakshaydumbre/JK-Project.git
    cd intelligent_book_manager
    ```

2.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate    # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup:**

    -   Ensure you have PostgreSQL installed and running.
    -   Create a database named `bookdb` (or whatever you've configured in `config/settings.py`).
    - Set up the DATABASE_URL in your .env file or in the config file. Example: `DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/bookdb"`

5. **Add environment variables**
    - create a .env file in the root directory and add environment variables

6.  **Run the Application:**

    ```bash
    uvicorn intelligent_book_manager.app.main:app --reload
    ```

    -   This will start the FastAPI server. You can access the API documentation at `http://127.0.0.1:8000/docs` (or the relevant address)

## API Endpoints

### Book Endpoints

-   **`POST /books`**
    -   Create a new book.
    -   Request Body:
        ```json
        {
            "title": "The Hitchhiker's Guide to the Galaxy",
            "author": "Douglas Adams",
            "genre": "Science Fiction",
            "year_published": 1979,
            "summary": "A novel about racial injustice in the Deep South, seen through the eyes of young Scout Finch."
        }
        ```
    - Response Body:
        ```json
        {
            "id": 1,
            "title": "The Hitchhiker's Guide to the Galaxy",
            "author": "Douglas Adams",
            "genre": "Science Fiction",
            "year_published": 1979,
            "summary": "A novel about racial injustice in the Deep South, seen through the eyes of young Scout Finch."
        }
        ```
-   **`GET /books`**
    -   Get all books.
-   **`GET /books/{book_id}`**
    -   Get a specific book by ID.
-   **`PUT /books/{book_id}`**
    -   Update a book.
    - request body is same as the POST request.
-   **`DELETE /books/{book_id}`**
    -   Delete a book.

### Review Endpoints

-   **`POST /books/{book_id}/reviews`**
    -   Add a review to a book.
    -   Request body:
        ```json
        {
            "user_id": 1,
            "review_text": "Great book!",
            "rating": 4.5
        }
        ```
-   **`GET /books/{book_id}/reviews`**
    -   Get all reviews for a book.
    - Response body:
      ```json
      [
        {
            "user_id": 1,
            "review_text": "Great book!",
            "rating": 4.5
        }
      ]
      ```

### Summary Endpoint

-   **`GET /books/{book_id}/summary`**
    -   Get the summary of a book (generates it if not present).
    - Response body
        ```json
        {
            "summary": "This is a summary"
        }
        ```

### Recommendation Endpoint

-   **`GET /recommendations`**
    -   Get book recommendations based on genre.
    - Response body:
        ```json
        [
        {
            "id": 1,
            "title": "The Hitchhiker's Guide to the Galaxy",
            "author": "Douglas Adams",
            "genre": "Science Fiction",
            "year_published": 1979,
            "summary": null
        },
        {
            "id": 2,
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "genre": "Romance",
            "year_published": 1813,
            "summary": null
        }
        ]
        ```

## Docker

1.  **Build the Docker image:**

    ```bash
    docker build -t intelligent-book-manager
    ```

2.  **Run the Docker container:**

    ```bash
    docker run -d -p 8000:8000 intelligent-book-manager
    ```

## Testing

-   We have included a sample test file.
-   To execute the unit tests:
    ```bash
    pytest -vv tests/test_main.py::test_create_book && sleep 1 \
    && pytest -vv tests/test_main.py::test_update_book && sleep 1 \
    && pytest -vv tests/test_main.py::test_get_books && sleep 1 \
    && pytest -vv tests/test_main.py::test_get_book_by_id && sleep 1 \
    && pytest -vv tests/test_main.py::test_delete_book && sleep 1 \
    && pytest -vv tests/test_main.py::test_add_review && sleep 1 \
    && pytest -vv tests/test_main.py::test_get_reviews && sleep 1 \
    && pytest -vv tests/test_main.py::test_get_summary && sleep 1 \
    && pytest -vv tests/test_main.py::test_get_recommendations
    ```

## Deployment

-   The `deploy/` directory contains a sample script, `aws_deploy.sh`, to give you an idea of how deployment might be handled.
-   You can customize these scripts for your target deployment environment (e.g., AWS, Heroku, etc.)

## Contributing

-   Contributions are welcome! Please feel free to fork the repository and submit pull requests.

## License

-   [MIT](LICENSE) (or add a different license if you prefer).