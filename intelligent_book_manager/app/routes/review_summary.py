from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from intelligent_book_manager.app.services.llama3_service import generate_review_summary

router = APIRouter()

class ReviewSummaryRequest(BaseModel):
    reviews: List[str]

@router.post("/generate-review-summary")
async def summarize_reviews(request: ReviewSummaryRequest):
    """
    API endpoint to generate a summary for multiple user reviews using LLaMA 3.
    """
    summary = generate_review_summary(request.reviews)
    if summary:
        return {"review_summary": summary}
    raise HTTPException(status_code=500, detail="Failed to generate review summary")