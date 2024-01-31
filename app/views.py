import psycopg2 
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user 

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    return render_template("home.html")
    
@views.route("/<username>")
@login_required
def show_user_profile(username):
    return render_template("user.html", user = username)

@views.route("/history")
@login_required
def search_history():
    return render_template("search_history.html")

@views.route("/saved")
@login_required
def saved_songs():
    return render_template("saved.html")
