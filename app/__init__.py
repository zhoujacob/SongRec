import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Load environment variables from .env file
    load_dotenv()  
    
    # Get environment variables
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Ensure all required environment variables are set
    if None in (DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY):
        raise ValueError("Missing required environment variables")

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"
    
    # Initialize database
    db.init_app(app) 
    
    # Register blueprints
    from .views import views
    from .auth import auth 
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User

    with app.app_context():
        from . import models
        models.create_database()  # Initialize the database

    return app