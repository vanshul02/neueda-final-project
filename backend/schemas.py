from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TransactionCreate(BaseModel):
    amount: float

class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    username: str
    balance: float

    class Config:
        orm_mode = True
