from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User 
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user 

auth = Blueprint("auth", __name__)

@auth.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Filters users by their email
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash ('Logged in successfully!', category = 'success')
                # Remembers until end of flask session
                login_user(user, remember = True)
                return redirect(url_for("views.home"))
            else:
                flash('Incorrect Password, please try again.', category = 'error')
        else:
            flash('Email does not exist.', category = 'success')

    else:
        return render_template("login.html", boolean = True)
    
@auth.route("/logout")
def logout():
    return "<p>Logout</p>"

@auth.route("/sign-up", methods = ["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        first_Name = request.form.get('firstName')
        password1 = request.form.get('password1') 
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category = 'error')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category = 'error') 
        elif len(first_Name) < 2:
            flash('First name must be greater than 1 character.', category = 'error')
        elif password1 != password2:
            flash('Password must match', category = 'error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters long', category = 'error') 
        else: 
            # sha265 hashihng algorithm through the werkzeug security import
            new_user = User(email = email, first_name = first_Name, password = generate_password_hash(password1, method='pbkdf2:sha256', salt_length=8))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember = True)
            flash('Account created!', category = 'success')
            # Redirect to home page after created
            return redirect(url_for('views.home'))
        return render_template("sign-up.html")
    else:
        return render_template("sign-up.html")
    