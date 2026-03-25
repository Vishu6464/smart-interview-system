from pydantic import BaseModel
from typing import List

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    difficulty: str

    class Config:
        from_attributes = True


class AnswerRequest(BaseModel):
    question_id: int
    user_answer: str


class AnalyticsResponse(BaseModel):
    total_attempts: int
    average_score: float