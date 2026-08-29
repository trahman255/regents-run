import hashlib
import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.domain import User
from schemas.pydantic import UserRegister, UserLogin, ForgotPassword, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return f"{salt}${pwd_hash}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    try:
        salt, pwd_hash = stored_password.split('$')
        check_hash = hashlib.sha256((provided_password + salt).encode('utf-8')).hexdigest()
        return check_hash == pwd_hash
    except Exception:
        return False

@router.post("/guest", response_model=UserResponse)
def create_guest_user(db: Session = Depends(get_db)):
    guest_username = f"guest_{secrets.token_hex(4)}"
    guest_user = User(username=guest_username, is_guest=True)
    db.add(guest_user)
    db.commit()
    db.refresh(guest_user)
    return guest_user

@router.post("/register", response_model=UserResponse)
def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.username == user_in.username) | (User.email == user_in.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered.")
    
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        username=user_in.username,
        password_hash=hash_password(user_in.password),
        is_guest=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=UserResponse)
def login_user(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_in.username).first()
    if not user or not user.password_hash or not verify_password(user.password_hash, user_in.password):
        raise HTTPException(status_code=400, detail="Invalid username or password.")
    return user

@router.post("/forgot-password")
def forgot_password(data: ForgotPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter((User.username == data.username_or_email) | (User.email == data.username_or_email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found with that username or email.")
    
    user.password_hash = hash_password(data.new_password)
    db.commit()
    return {"status": "success", "message": "Password successfully updated."}