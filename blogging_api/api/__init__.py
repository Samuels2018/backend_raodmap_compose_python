from flask import Flask
from flask_pymongo import PyMongo
from api.config import Config

mongo = PyMongo()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)
  
  mongo.init_app(app)
  
  from api.resources.posts import posts_bp
  app.register_blueprint(posts_bp)
  
  return app