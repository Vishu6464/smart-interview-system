from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal
import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/analytics")
def analytics(category: str = "coding", db: Session = Depends(get_db)):

    # Join attempts with questions (no N+1 problem)
    results = (
        db.query(models.Attempt, models.Question)
        .join(models.Question, models.Attempt.question_id == models.Question.id)
        .filter(models.Question.category == category)
        .all()
    )

    if not results:
        return {
            "total_attempts": 0,
            "average_score": 0,
            "domain_performance": {},
            "difficulty_breakdown": {}
        }

    total_attempts = len(results)
    avg_score = sum(attempt.score for attempt, _ in results) / total_attempts

    domain_scores = {}
    difficulty_counts = {}

    for attempt, question in results:

        # Domain performance
        if question.domain not in domain_scores:
            domain_scores[question.domain] = []
        domain_scores[question.domain].append(attempt.score)

        # Difficulty breakdown
        if question.difficulty not in difficulty_counts:
            difficulty_counts[question.difficulty] = 0
        difficulty_counts[question.difficulty] += 1

    domain_avg = {
        domain: round(sum(scores) / len(scores), 2)
        for domain, scores in domain_scores.items()
    }

    return {
        "total_attempts": total_attempts,
        "average_score": round(avg_score, 2),
        "domain_performance": domain_avg,
        "difficulty_breakdown": difficulty_counts
    }
