from intelligent_book_manager.app.routes import auth, book_routes, summary, review_summary
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
            title="Intelligent Book Management System",
            description="API for managing books and reviews",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],  # Restrict to specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(book_routes.router)
app.include_router(summary.router)
app.include_router(review_summary.router)