from datetime import date
from enum import Enum
from pydantic import BaseModel
from typing import Optional, List

class ExpenseCategory(str, Enum):
  GROCERIES = "Groceries"
  LEISURE = "Leisure"
  ELECTRONICS = "Electronics"
  UTILITIES = "Utilities"
  CLOTHING = "Clothing"
  HEALTH = "Health"
  OTHERS = "Others"

class ExpenseBase(BaseModel):
  amount: float
  description: Optional[str] = None
  category: ExpenseCategory = ExpenseCategory.OTHERS
  date: date = date.today()

class ExpenseCreate(ExpenseBase):
  pass

class Expense(ExpenseBase):
  id: int
  owner_id: int

  class Config:
    from_attributes = True

class UserBase(BaseModel):
  username: str
  email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
  id: int
  is_active: bool
  expenses: List[Expense] = []

  class Config:
    from_attributes = True

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: Optional[str] = None

class ExpenseFilter(BaseModel):
  period: Optional[str] = None  # "week", "month", "3months"
  start_date: Optional[date] = None
  end_date: Optional[date] = None
  category: Optional[ExpenseCategory] = None