from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class UserBase(BaseModel):
    username: str
    email: str
    alamat: str | None = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: str

    class Config:
        from_attributes = True

class TransactionCategory(str, Enum):
    PENGELUARAN = "PENGELUARAN"
    PEMASUKAN = "PEMASUKAN"

class TransactionBase(BaseModel):
    amount: int
    description: str | None = None
    date: datetime | None = None
    category: TransactionCategory

class TransactionCreate(TransactionBase):
    userId: str

class TransactionResponse(TransactionBase):
    id: str
    userId: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
