from sqlalchemy.orm import Session
from datetime import date, timedelta
from models import models 
from schemas import schemas

def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
  return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
  return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
  fake_hashed_password = user.password + "notreallyhashed"
  db_user = models.User(
    username=user.username,
    email=user.email,
    hashed_password=fake_hashed_password
  )
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

def get_expenses(db: Session, user_id: int, skip: int = 0, limit: int = 100):
  return (
    db.query(models.Expense)
    .filter(models.Expense.owner_id == user_id)
    .offset(skip)
    .limit(limit)
    .all()
  )

def filter_expenses(db: Session, user_id: int, filters: schemas.ExpenseFilter):
  query = db.query(models.Expense).filter(models.Expense.owner_id == user_id)
  
  today = date.today()
  
  if filters.period:
    if filters.period == "week":
      start_date = today - timedelta(days=7)
      query = query.filter(models.Expense.date >= start_date)
    elif filters.period == "month":
      start_date = today - timedelta(days=30)
      query = query.filter(models.Expense.date >= start_date)
    elif filters.period == "3months":
      start_date = today - timedelta(days=90)
      query = query.filter(models.Expense.date >= start_date)
  
  if filters.start_date:
    query = query.filter(models.Expense.date >= filters.start_date)
  
  if filters.end_date:
    query = query.filter(models.Expense.date <= filters.end_date)
  
  if filters.category:
    query = query.filter(models.Expense.category == filters.category)
  
  return query.all()

def create_user_expense(db: Session, expense: schemas.ExpenseCreate, user_id: int):
  db_expense = models.Expense(**expense.model_dump(), owner_id=user_id)
  db.add(db_expense)
  db.commit()
  db.refresh(db_expense)
  return db_expense

def get_expense(db: Session, expense_id: int, user_id: int):
  return (
    db.query(models.Expense)
    .filter(models.Expense.id == expense_id, models.Expense.owner_id == user_id)
    .first()
  )

def update_expense(db: Session, expense_id: int, expense: schemas.ExpenseCreate, user_id: int):
  db_expense = get_expense(db, expense_id, user_id)
  if db_expense:
    for key, value in expense.model_dump().items():
      setattr(db_expense, key, value)
    db.commit()
    db.refresh(db_expense)
  return db_expense

def delete_expense(db: Session, expense_id: int, user_id: int):
  db_expense = get_expense(db, expense_id, user_id)
  if db_expense:
    db.delete(db_expense)
    db.commit()
  return db_expense