from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
  database_name: str = os.environ.get('DATABASE_NAME', 'expense_tracker')
  database_username: str = os.environ.get('DATABASE_USERNAME', 'username')
  database_password: str = os.environ.get('DATABASE_PASSWORD', 'password')
  database_host: str = os.environ.get('DATABASE_HOST_CONTAINER', 'localhost')
  database_port: str = os.environ.get('DATABASE_PORT', '5432')
  secret_key: str = "your-secret-key-here"
  algorithm: str = "HS256"
  access_token_expire_minutes: int = 30

  class Config:
    env_file = ".env"

settings = Settings()