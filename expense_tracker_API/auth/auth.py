from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from schemas import schemas
from models import models 
from tracker import crud
from db import SessionLocal
from settings import settings
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str):
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
  return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
  user = crud.get_user_by_username(db, username)
  if not user:
    return False
  if not verify_password(password, user.hashed_password):
    return False
  return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
  return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
    token_data = schemas.TokenData(username=username)
  except JWTError:
    raise credentials_exception
  
  db = SessionLocal()
  user = crud.get_user_by_username(db, username=token_data.username)
  db.close()
  if user is None:
    raise credentials_exception
  return user

async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
  if not current_user.is_active:
    raise HTTPException(status_code=400, detail="Inactive user")
  return current_user