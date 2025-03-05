from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from intelligent_book_manager.app.services.llama3_service import generate_summary

router = APIRouter()

class SummaryRequest(BaseModel):
    text: str

@router.post("/generate-summary")
def generate_summary_endpoint(request: SummaryRequest):
    """
    API endpoint to generate a summary for a given text using Hugging Face Transformers.
    """
    summary = generate_summary(request.text)  # ❌ Don't use 'await' here (function is not async)
    if "Error" in summary:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {summary}")
    return {"summary": summary}