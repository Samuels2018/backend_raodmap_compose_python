from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import date, timedelta
from sqlalchemy.orm import Session

from models import models
from schemas import schemas 
from tracker import crud 
from auth import auth
from db import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  db_user = crud.get_user_by_email(db, email=user.email)
  if db_user:
    raise HTTPException(status_code=400, detail="Email already registered")
  db_user = crud.get_user_by_username(db, username=user.username)
  if db_user:
    raise HTTPException(status_code=400, detail="Username already taken")
  return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
  form_data: OAuth2PasswordRequestForm = Depends(),
  db: Session = Depends(get_db)
):
  user = auth.authenticate_user(db, form_data.username, form_data.password)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )
  access_token_expires = timedelta(minutes=auth.settings.access_token_expire_minutes)
  access_token = auth.create_access_token(
    data={"sub": user.username}, expires_delta=access_token_expires
  )
  return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_active_user)):
  return current_user

@app.get("/expenses/", response_model=List[schemas.Expense])
def read_expenses(
  skip: int = 0,
  limit: int = 100,
  current_user: schemas.User = Depends(auth.get_current_active_user),
  db: Session = Depends(get_db)
):
  expenses = crud.get_expenses(db, user_id=current_user.id, skip=skip, limit=limit)
  return expenses

@app.post("/expenses/filter", response_model=List[schemas.Expense])
def filter_expenses(
  filter: schemas.ExpenseFilter,
  current_user: schemas.User = Depends(auth.get_current_active_user),
  db: Session = Depends(get_db)
):
  expenses = crud.filter_expenses(db, user_id=current_user.id, filters=filter)
  return expenses

@app.post("/expenses/", response_model=schemas.Expense)
def create_expense(
  expense: schemas.ExpenseCreate,
  current_user: schemas.User = Depends(auth.get_current_active_user),
  db: Session = Depends(get_db)
):
  return crud.create_user_expense(db=db, expense=expense, user_id=current_user.id)

@app.get("/expenses/{expense_id}", response_model=schemas.Expense)
def read_expense(
  expense_id: int,
  current_user: schemas.User = Depends(auth.get_current_active_user),
  db: Session = Depends(get_db)
):
  db_expense = crud.get_expense(db, expense_id=expense_id, user_id=current_user.id)
  if db_expense is None:
    raise HTTPException(status_code=404, detail="Expense not found")
  return db_expense

@app.put("/expenses/{expense_id}", response_model=schemas.Expense)
def update_expense(
  expense_id: int,
  expense: schemas.ExpenseCreate,
  current_user: schemas.User = Depends(auth.get_current_active_user),
  db: Session = Depends(get_db)
):
  db_expense = crud.update_expense(db, expense_id=expense_id, expense=expense, user_id=current_user.id)
  if db_expense is None:
    raise HTTPException(status_code=404, detail="Expense not found")
  return db_expense

@app.delete("/expenses/{expense_id}", response_model=schemas.Expense)
def delete_expense(
  expense_id: int,
  current_user: schemas.User = Depends(auth.get_current_active_user),
  db: Session = Depends(get_db)
):
  db_expense = crud.delete_expense(db, expense_id=expense_id, user_id=current_user.id)
  if db_expense is None:
    raise HTTPException(status_code=404, detail="Expense not found")
  return db_expense