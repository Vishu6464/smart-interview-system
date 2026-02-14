from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, index=True)
    difficulty = Column(String)
    question_text = Column(Text)
    ideal_answer = Column(Text)


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_answer = Column(Text)
    score = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())