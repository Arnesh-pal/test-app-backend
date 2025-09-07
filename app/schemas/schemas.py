# app/schemas/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- Authentication Schemas (Original) ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# --- Exam Schemas (New) ---

class Answer(BaseModel):
    question_id: int
    selected_answer: str

class ExamSubmit(BaseModel):
    answers: List[Answer]

class Question(BaseModel):
    id: int
    question_text: str
    options: List[str]

    class Config:
        from_attributes = True

class ExamResult(BaseModel):
    id: int
    user_id: int
    score: int
    submitted_at: datetime

    class Config:
        from_attributes = True

class DetailedResult(BaseModel):
    question_text: str
    options: List[str]
    your_answer: str
    correct_answer: str
    is_correct: bool

class SubmissionResponse(BaseModel):
    score: int
    total: int
    detailed_results: List[DetailedResult]

# app/schemas/schemas.py

# Models for saving exam results from the frontend
class AnsweredQuestionCreate(BaseModel):
    question_text: str
    your_answer: str
    correct_answer: str
    is_correct: bool
    isMultipleChoice: bool # We don't save this, but it's in the payload
    options: List[str] # Also not saved, but in the payload

class ExamResultCreate(BaseModel):
    topic: Optional[str]
    score: int
    total: int
    detailed_results: List[AnsweredQuestionCreate]

# Models for sending history data to the frontend
class TopicStat(BaseModel):
    topic: str
    correct: int
    incorrect: int
    total: int

class ExamHistoryItem(BaseModel):
    id: int
    topic: Optional[str]
    score: int
    total_questions: int
    submitted_at: datetime

    class Config:
        from_attributes = True

class HistoryResponse(BaseModel):
    attempts: List[ExamHistoryItem]
    topic_stats: List[TopicStat]

class AnsweredQuestionDetail(BaseModel):
    question_text: str
    your_answer: str
    correct_answer: str
    is_correct: bool

    class Config:
        from_attributes = True