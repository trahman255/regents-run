from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- User & Auth Schemas ---
class UserRegister(BaseModel):
    name: str
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ForgotPassword(BaseModel):
    username_or_email: str
    new_password: str

class UserResponse(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    username: str
    is_guest: bool

    class Config:
        from_attributes = True

# --- Question & Test Schemas ---
class QuestionOut(BaseModel):
    id: int
    course: str
    topic: str
    question: str
    options: Optional[List[str]] = None
    answer: Optional[str] = None       # <-- Added this!
    image_url: Optional[str] = None    # <-- Added this!

    class Config:
        from_attributes = True

# --- Progress & Analytics Schemas ---
class SubmitAnswer(BaseModel):
    user_id: int
    question_id: int
    is_correct: bool

class SubjectStat(BaseModel):
    course: str
    total_attempted: int
    total_correct: int
    accuracy_percentage: float