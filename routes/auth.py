from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserLogin, UserResponse
from utils import hash_password, verify_password
from database import get_db
import uuid
from logger import log_info, log_error

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        log_error(f"Registrasi gagal: Email {user.email} sudah terdaftar")
        raise HTTPException(status_code=400, detail={"message": "Email already registered"})
    
    hashed_password = hash_password(user.password)
    new_user = User(
        id=str(uuid.uuid4()),
        username=user.username,
        email=user.email,
        password=hashed_password,
        alamat=user.alamat
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    log_info(f"Registrasi berhasil: {user.email}")
    return {
        "code": 201,
        "success": True,
        "message": "Registration successful"
    }

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user:
        log_error(f"Login gagal: User {user.email} tidak ditemukan")
        raise HTTPException(status_code=404, detail={"message": "User not found"})

    if not verify_password(user.password, db_user.password):
        log_error(f"Login gagal: Password salah untuk {user.email}")
        raise HTTPException(status_code=401, detail={"message": "Invalid email or password"})

    log_info(f"Login berhasil: {user.email}")
    return {
        "code": 200,
        "success": True,
        "message": "Login successful",
        "data": {
            "username": db_user.username,
            "email": db_user.email,
            "alamat": db_user.alamat
        }
    }
