import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  mongo_db = os.getenv('MONGO_DB', 'blogging_platform')
  mongo_db_host_container = os.getenv('MONGO_DB_HOST_CONTAINER', 'localhost')
  mongo_db_port = os.getenv('MONGO_DB_PORT', '27017')
  MONGO_URI = f'mongodb://{mongo_db_host_container}:{mongo_db_port}/{mongo_db}'

  SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')