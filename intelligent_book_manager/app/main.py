from fastapi import FastAPI
from intelligent_book_manager.app.routes import book_routes, summary, review_summary

app = FastAPI(title="Intelligent Book Management System")

app.include_router(book_routes.router)
app.include_router(summary.router)
app.include_router(review_summary.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Intelligent Book Management System"}

@app.get("/")
def home():
    return {"message": "Welcome to the Intelligent Book Manager API"}