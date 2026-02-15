from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas
from services.scoring_service import calculate_score

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/answer")
def submit_answer(answer: schemas.AnswerRequest, db: Session = Depends(get_db)):

    question = db.query(models.Question).filter(
        models.Question.id == answer.question_id
    ).first()

    if not question:
        return {"error": "Question not found"}

    score = calculate_score(answer.user_answer, question.ideal_answer)

    attempt = models.Attempt(
        question_id=answer.question_id,
        user_answer=answer.user_answer,
        score=score
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt.id,
        "score": score,
        "category": question.category,
        "difficulty": question.difficulty
    }