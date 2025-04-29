from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import date
from enum import Enum as PyEnum

from db import Base

class ExpenseCategory(str, PyEnum):
  GROCERIES = "Groceries"
  LEISURE = "Leisure"
  ELECTRONICS = "Electronics"
  UTILITIES = "Utilities"
  CLOTHING = "Clothing"
  HEALTH = "Health"
  OTHERS = "Others"

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  username = Column(String, unique=True, index=True)
  email = Column(String, unique=True, index=True)
  hashed_password = Column(String)

  expenses = relationship("Expense", back_populates="owner")

class Expense(Base):
  __tablename__ = "expenses"

  id = Column(Integer, primary_key=True, index=True)
  amount = Column(Float, nullable=False)
  description = Column(String)
  category = Column(Enum(ExpenseCategory), default=ExpenseCategory.OTHERS)
  date = Column(Date, default=date.today())
  owner_id = Column(Integer, ForeignKey("users.id"))

  owner = relationship("User", back_populates="expenses")