from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models import Review
from app.core.security import verify_token

router = APIRouter()

class CodeReviewRequest(BaseModel):
    code: str
    filename: Optional[str] = "code.py"
    token: str

class FeedbackRequest(BaseModel):
    review_id: int
    feedback: str
    token: str

@router.post("/analyze")
async def analyze_code(request: CodeReviewRequest, db: Session = Depends(get_db)):
    payload = verify_token(request.token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    from app.agents.orchestrator import run_review
    result = await run_review(request.code, request.filename)

    review = Review(
        user_id=1,
        filename=request.filename,
        original_code=request.code,
        quality_score=result["scores"]["quality"],
        security_score=result["scores"]["security"],
        readability_score=result["scores"]["readability"],
        overall_score=result["scores"]["overall"],
        issues=str(result["issues"]),
        suggestions=str(result["suggestions"]),
        severity=result["severity"]
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    return {
        "review_id": review.id,
        "scores": result["scores"],
        "issues": result["issues"],
        "suggestions": result["suggestions"],
        "severity": result["severity"],
        "learning_tips": result["learning_tips"]
    }

@router.get("/history")
def get_review_history(token: str, db: Session = Depends(get_db)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    reviews = db.query(Review).order_by(Review.created_at.desc()).limit(10).all()
    return {"reviews": [
        {
            "id": r.id,
            "filename": r.filename,
            "overall_score": r.overall_score,
            "severity": r.severity,
            "created_at": str(r.created_at)
        } for r in reviews
    ]}

@router.post("/feedback")
def submit_feedback(request: FeedbackRequest, db: Session = Depends(get_db)):
    payload = verify_token(request.token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    review = db.query(Review).filter(Review.id == request.review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review.feedback = request.feedback
    db.commit()
    return {"message": "Feedback submitted successfully"}