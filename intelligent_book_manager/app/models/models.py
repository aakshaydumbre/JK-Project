from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, index=True, nullable=False)
    year_published = Column(Integer, nullable=False)
    summary = Column(String, nullable=True)

    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(String, nullable=False)
    review_text = Column(String, nullable=False)
    rating = Column(Float, nullable=False)

    book = relationship("Book", back_populates="reviews")