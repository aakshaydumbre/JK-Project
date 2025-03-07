from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from intelligent_book_manager.app.database import Base
from pydantic import BaseModel

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, index=True, nullable=False)
    year_published = Column(Integer, nullable=False)
    summary = Column(String, nullable=True)

    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None