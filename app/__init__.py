import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager

db = SQLAlchemy()
load_dotenv()  


def create_app():
    app = Flask(__name__)

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

    login_manager = LoginManager()
    # If user is not logged in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Retrieves the ID of the user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app