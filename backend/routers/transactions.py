from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from database import SessionLocal
from models import User, Transaction
from schemas import TransactionCreate, TransactionResponse
from typing import List

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/", response_model=List[TransactionResponse])
def get_transaction_history(token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    transactions = db.query(Transaction).filter(Transaction.user_id == user.id).all()
    return transactions

@router.post("/deposit", response_model=TransactionResponse)
def deposit(transaction: TransactionCreate, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    new_transaction = Transaction(user_id=user.id, amount=transaction.amount, type="deposit")
    user.balance += transaction.amount
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@router.post("/withdraw", response_model=TransactionResponse)
def withdraw(transaction: TransactionCreate, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    if user.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    new_transaction = Transaction(user_id=user.id, amount=-transaction.amount, type="withdraw")
    user.balance -= transaction.amount
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction
