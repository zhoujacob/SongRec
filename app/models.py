import psycopg2
import os
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from dotenv import load_dotenv

load_dotenv()  

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

# class for saved songs 
class Saved(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database = os.environ['DB_NAME'],
                            user = os.environ['DB_USER'],
                            password = os.environ['DB_PASSWORD'])
    return conn

def create_database():
    db.create_all()  # Create the database tables
    print('Created Database!')
