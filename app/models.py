from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

def create_database():
    db.create_all()  # Create the database tables
    print('Created Database!')


# class for saved history
# class Note(db.Model):
    # id = db.Column(db.Integer, priamry_key = True)
    # data = db.Column
    # date = db.Column(db.DateTime(timezone = True), default = func.now())
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
