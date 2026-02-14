from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import random

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/question/{domain}")
def get_question(domain: str, difficulty: str = None, db: Session = Depends(get_db)):

    query = db.query(models.Question).filter(models.Question.domain == domain)

    if difficulty:
        query = query.filter(models.Question.difficulty == difficulty)

    questions = query.all()

    if not questions:
        return {"error": "No questions found"}

    return random.choice(questions)


@router.get("/mock/{domain}")
def mock_interview(domain: str, db: Session = Depends(get_db)):

    questions = db.query(models.Question).filter(
        models.Question.domain == domain
    ).all()

    random.shuffle(questions)

    return questions[:5]