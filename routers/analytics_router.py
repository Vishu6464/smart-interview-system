from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
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
def analytics(db: Session = Depends(get_db)):

    attempts = db.query(models.Attempt).all()

    if not attempts:
        return {
            "total_attempts": 0,
            "average_score": 0,
            "domain_performance": {}
        }

    total_attempts = len(attempts)
    avg_score = sum(a.score for a in attempts) / total_attempts

    domain_scores = {}

    for attempt in attempts:
        question = db.query(models.Question).filter(
            models.Question.id == attempt.question_id
        ).first()

        domain = question.domain

        if domain not in domain_scores:
            domain_scores[domain] = []

        domain_scores[domain].append(attempt.score)

    domain_avg = {
        domain: round(sum(scores) / len(scores), 2)
        for domain, scores in domain_scores.items()
    }

    return {
        "total_attempts": total_attempts,
        "average_score": round(avg_score, 2),
        "domain_performance": domain_avg
    }