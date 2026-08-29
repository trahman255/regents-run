from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from sqlalchemy import Integer  # <-- Add Integer here!
from typing import List
from core.database import get_db
from models.domain import Question, UserProgress
from schemas.pydantic import QuestionOut, SubmitAnswer, SubjectStat

router = APIRouter(prefix="/tests", tags=["Tests"])

# 1. 24-Question Mixed Exam
@router.get("/mixed", response_model=List[QuestionOut])
def get_mixed_test(course: str = "Algebra II", db: Session = Depends(get_db)):
    return (
        db.query(Question)
        .filter(Question.course == course)
        .order_by(func.random())
        .limit(24)
        .all()
    )

# 2. Topic-wise Test
@router.get("/topic/{topic_name}", response_model=List[QuestionOut])
def get_topic_test(topic_name: str, db: Session = Depends(get_db)):
    return db.query(Question).filter(Question.topic == topic_name).all()

# 3. Submit an Answer Attempt
@router.post("/submit")
def submit_answer(attempt: SubmitAnswer, db: Session = Depends(get_db)):
    progress_entry = UserProgress(
        user_id=attempt.user_id,
        question_id=attempt.question_id,
        is_correct=attempt.is_correct
    )
    db.add(progress_entry)
    db.commit()
    return {"status": "success", "recorded": True}

# 4. Practice Missed / Wrong Questions
@router.get("/review/{user_id}", response_model=List[QuestionOut])
def get_incorrect_questions(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Question)
        .join(UserProgress, Question.id == UserProgress.question_id)
        .filter(
            UserProgress.user_id == user_id,
            UserProgress.is_correct == False
        )
        .distinct()
        .all()
    )

# 5. User Performance & Accuracy Stats by Subject
@router.get("/stats/{user_id}", response_model=List[SubjectStat])
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    attempts = (
        db.query(
            Question.course,
            func.count(UserProgress.id).label("total"),
            func.sum(func.cast(UserProgress.is_correct, Integer)).label("correct")
        )
        .join(Question, Question.id == UserProgress.question_id)
        .filter(UserProgress.user_id == user_id)
        .group_by(Question.course)
        .all()
    )

    results = []
    for course, total, correct in attempts:
        correct_count = correct or 0
        accuracy = round((correct_count / total) * 100, 2) if total > 0 else 0.0
        results.append(
            SubjectStat(
                course=course,
                total_attempted=total,
                total_correct=correct_count,
                accuracy_percentage=accuracy
            )
        )
    return results