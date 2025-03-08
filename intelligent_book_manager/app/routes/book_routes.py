from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from intelligent_book_manager.app.services.auth import get_current_user
from intelligent_book_manager.app.database import get_db
from intelligent_book_manager.app.models.models import Book, Review
from pydantic import BaseModel
from typing import List, Optional, Dict
from intelligent_book_manager.app.services.llama3_service import generate_summary
import asyncio
from typing import Optional
from fastapi import Query
from collections import defaultdict

router = APIRouter()

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None

class BookResponse(BookCreate):
    id: int
    summary: Optional[str] = None

class ReviewCreate(BaseModel):
    user_id: str
    review_text: str
    rating: float

class ReviewResponse(ReviewCreate):
    book_id: int


@router.post("/books", response_model=BookResponse)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    # new_book = Book(**book.dict())
    new_book = Book(**book.model_dump()) #this line added while test case and above is the previously working.
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

@router.get("/books", response_model=List[BookResponse])
async def get_books(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)):
    result = await db.execute(select(Book))
    return result.scalars().all()

@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter(Book.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/books/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, book_data: BookCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter(Book.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_data.dict().items():
        setattr(book, key, value)

    await db.commit()
    await db.refresh(book)
    return book

@router.delete("/books/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter(Book.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    await db.delete(book)
    await db.commit()
    return {"message": "Book deleted successfully"}

@router.post("/books/{book_id}/reviews")
async def add_review(book_id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter(Book.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    new_review = Review(book_id=book_id, **review.dict())
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)  # ✅ Fix: Refresh the inserted review
    return {"message": "Review added successfully"}

@router.get("/books/{book_id}/reviews", response_model=List[ReviewResponse])
async def get_reviews(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).filter(Review.book_id == book_id))
    reviews = result.scalars().all()

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this book")

    return reviews

@router.get("/books/{book_id}/summary")
async def get_book_summary(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter(Book.id == book_id))
    book = result.scalars().first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not book.summary:
        book.summary = await generate_summary(book.title + " by " + book.author)
        await db.commit()
        await db.refresh(book)

    return {"summary": book.summary}

@router.get("/recommendations")
async def get_recommendations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    books = result.scalars().all()

    # Group books by genre asynchronously
    genres: Dict[str, List[Book]] = defaultdict(list)

    for book in books:
        genres[book.genre].append(book)

    # Select one book per genre asynchronously
    recommended_books = [books[0] for books in genres.values() if books]

    return recommended_books