from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from typing import List
from database import get_db
from models import Transaction
from schemas import TransactionCreate, TransactionResponse

router = APIRouter()

@router.get("/", response_model=dict)
async def get_transactions(userId: str, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.userId == userId).all()

    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for the given userId")

    total_income = sum(t.amount for t in transactions if t.category == "PEMASUKAN")
    total_expense = sum(t.amount for t in transactions if t.category == "PENGELUARAN")
    total_balance = total_income - total_expense

    return {
        "code": 200,
        "success": True,
        "message": "Transactions retrieved successfully",
        "data": transactions,
        "metadata": {
            "total_saldo": total_balance,
            "total_pengeluaran": total_expense,
            "total_pemasukan": total_income,
        }
    }

@router.post("/", response_model=TransactionResponse, status_code=201)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    new_transaction = Transaction(
        id=str(uuid4()), 
        amount=transaction.amount,
        description=transaction.description,
        date=transaction.date or datetime.now(),
        userId=transaction.userId,
        category=transaction.category,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction

@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(transaction_id: str, transaction: TransactionCreate, db: Session = Depends(get_db)):
    existing_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    existing_transaction.amount = transaction.amount
    existing_transaction.description = transaction.description
    existing_transaction.date = transaction.date or existing_transaction.date
    existing_transaction.category = transaction.category
    existing_transaction.updated_at = datetime.now()

    db.commit()
    db.refresh(existing_transaction)

    return existing_transaction

@router.delete("/{transaction_id}", response_model=dict)
async def delete_transaction(transaction_id: str, userId: str, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.userId == userId).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found or unauthorized")

    db.delete(transaction)
    db.commit()

    return {
        "code": 200,
        "success": True,
        "message": "Transaction deleted successfully"
    }
