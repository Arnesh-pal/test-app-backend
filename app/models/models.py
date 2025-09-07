# app/models/models.py
from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    attempts = relationship("ExamAttempt", back_populates="user")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    correct_answer = Column(String, nullable=False)

# NEW: Represents a single exam sitting
class ExamAttempt(Base):
    __tablename__ = "exam_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String, nullable=True) # The topic of the exam
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="attempts")
    answered_questions = relationship("AnsweredQuestion", back_populates="attempt")

# NEW: Represents a single answered question within an attempt
class AnsweredQuestion(Base):
    __tablename__ = "answered_questions"
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("exam_attempts.id"))
    question_text = Column(Text)
    your_answer = Column(String) # For simplicity, we'll store joined multiple answers as a string
    correct_answer = Column(String)
    is_correct = Column(Boolean)
    topic = Column(String, index=True) # Storing topic here makes aggregation easy
    
    attempt = relationship("ExamAttempt", back_populates="answered_questions")