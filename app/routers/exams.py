# app/routers/exams.py
import os
import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List, Optional

from ..core import security
from ..schemas import schemas
from ..models import models, database

router = APIRouter(prefix="/exams", tags=["Exams"])

@router.get("/topics", response_model=List[str])
def get_topics():
    return ["Linux", "DevOps", "Code", "JavaScript", "Python", "HTML", "MySQL"]

@router.get("/start")
def start_exam(
    current_user: schemas.User = Depends(security.get_current_user),
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    limit: int = 5
):
    API_KEY = os.getenv("QUIZ_API_KEY")
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key is not configured.")

    params = {"apiKey": API_KEY, "limit": limit}
    if topic:
        params["tags"] = topic
    if difficulty:
        params["difficulty"] = difficulty

    try:
        response = requests.get("https://quizapi.io/api/v1/questions", params=params)
        response.raise_for_status()
        quiz_data = response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch questions from QuizAPI: {e}")

    formatted_questions = []
    if isinstance(quiz_data, list):
        for q in quiz_data:
            options = [v for k, v in q["answers"].items() if v is not None]
            correct_answers_list = [
                q["answers"][key.replace("_correct", "")]
                for key, is_correct in q["correct_answers"].items()
                if is_correct == "true" and q["answers"].get(key.replace("_correct", "")) is not None
            ]
            formatted_questions.append({
                "id": q["id"],
                "question_text": q["question"],
                "options": options,
                "isMultipleChoice": q.get("multiple_correct_answers") == "true",
                "correctAnswers": correct_answers_list 
            })
    return formatted_questions

@router.post("/save_result")
def save_result(
    result_data: schemas.ExamResultCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(security.get_current_user)
):
    new_attempt = models.ExamAttempt(
        user_id=current_user.id,
        topic=result_data.topic,
        score=result_data.score,
        total_questions=result_data.total
    )
    db.add(new_attempt)
    db.commit()
    db.refresh(new_attempt)

    for detail in result_data.detailed_results:
        answered_q = models.AnsweredQuestion(
            attempt_id=new_attempt.id,
            question_text=detail.question_text,
            your_answer=detail.your_answer,
            correct_answer=detail.correct_answer,
            is_correct=detail.is_correct,
            topic=result_data.topic or "Mixed"
        )
        db.add(answered_q)
    db.commit()
    return result_data

@router.get("/history", response_model=schemas.HistoryResponse)
def get_history(
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(security.get_current_user)
):
    attempts = db.query(models.ExamAttempt).filter(models.ExamAttempt.user_id == current_user.id).order_by(models.ExamAttempt.submitted_at.desc()).all()
    stats = db.query(
        models.AnsweredQuestion.topic,
        func.count(models.AnsweredQuestion.id).label("total"),
        func.sum(case((models.AnsweredQuestion.is_correct, 1), else_=0)).label("correct")
    ).join(models.ExamAttempt).filter(models.ExamAttempt.user_id == current_user.id).group_by(models.AnsweredQuestion.topic).all()
    topic_stats = [{"topic": stat.topic, "total": stat.total, "correct": stat.correct, "incorrect": stat.total - stat.correct} for stat in stats]
    return {"attempts": attempts, "topic_stats": topic_stats}

@router.get("/history/{attempt_id}", response_model=List[schemas.AnsweredQuestionDetail])
def get_attempt_details(
    attempt_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(security.get_current_user)
):
    attempt = db.query(models.ExamAttempt).filter(
        models.ExamAttempt.id == attempt_id,
        models.ExamAttempt.user_id == current_user.id
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Exam attempt not found.")

    answered_questions = db.query(models.AnsweredQuestion).filter(models.AnsweredQuestion.attempt_id == attempt_id).all()
    return answered_questions