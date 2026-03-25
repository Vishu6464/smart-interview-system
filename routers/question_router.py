from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from database import SessionLocal
import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/question/{domain}")
def get_question(
    domain: str,
    difficulty: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(models.Question).filter(
        models.Question.domain == domain,
        models.Question.category == "coding"  # IMPORTANT
    )

    if difficulty:
        query = query.filter(models.Question.difficulty == difficulty)

    question = query.order_by(func.random()).first()

    if not question:
        return {"error": "No coding questions found"}

    return question

@router.get("/mock/{domain}")
def mock_interview(
    domain: str,
    limit: int = 5,
    db: Session = Depends(get_db)
):

    questions = (
        db.query(models.Question)
        .filter(
            models.Question.domain == domain,
            models.Question.category == "mock"   # IMPORTANT
        )
        .order_by(func.random())
        .limit(limit)
        .all()
    )

    if not questions:
        return {"error": "No mock interview questions found"}

    return questions


@router.get("/mock-balanced/{domain}")
def mock_interview_balanced(
    domain: str,
    db: Session = Depends(get_db)
):

    easy = db.query(models.Question).filter(
        models.Question.domain == domain,
        models.Question.category == "mock",
        models.Question.difficulty == "Easy"
    ).order_by(func.random()).limit(1).all()

    medium = db.query(models.Question).filter(
        models.Question.domain == domain,
        models.Question.category == "mock",
        models.Question.difficulty == "Medium"
    ).order_by(func.random()).limit(2).all()

    hard = db.query(models.Question).filter(
        models.Question.domain == domain,
        models.Question.category == "mock",
        models.Question.difficulty == "Hard"
    ).order_by(func.random()).limit(1).all()

    return easy + medium + hard
