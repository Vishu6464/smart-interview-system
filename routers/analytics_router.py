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
def analytics(category: str = None, db: Session = Depends(get_db)):

    query = (
        db.query(models.Attempt, models.Question)
        .join(models.Question, models.Attempt.question_id == models.Question.id)
    )

    if category:
        query = query.filter(models.Question.category == category)

    results = query.all()

    if not results:
        return {
            "total_attempts": 0,
            "average_score": 0,
            "domain_performance": {},
            "difficulty_breakdown": {},
        }

    total_attempts = len(results)
    avg_score = sum(a.score for a, _ in results) / total_attempts

    domain_scores = {}
    difficulty_scores = {}
    difficulty_counts = {}

    for attempt, question in results:

        domain_scores.setdefault(question.domain, []).append(attempt.score)

        difficulty_scores.setdefault(question.difficulty, []).append(attempt.score)
        difficulty_counts[question.difficulty] = difficulty_counts.get(question.difficulty, 0) + 1

    domain_avg = {
        domain: round(sum(scores) / len(scores), 2)
        for domain, scores in domain_scores.items()
    }

    difficulty_avg = {
        difficulty: round(sum(scores) / len(scores), 2)
        for difficulty, scores in difficulty_scores.items()
    }

    return {
        "total_attempts": total_attempts,
        "average_score": round(avg_score, 2),
        "domain_performance": domain_avg,
        "difficulty_breakdown": difficulty_counts,
        "difficulty_average_score": difficulty_avg
    }
