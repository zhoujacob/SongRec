import psycopg2 
from flask import Blueprint, render_template, request, redirect, url_for
from scripts.init_db import show_users

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")
    
@views.route("/<username>")
def show_user_profile(username):
    return render_template("user.html", user = username)

@views.route("/history")
def search_history():
    return render_template("search_history.html")

@views.route("/saved")
def saved_songs():
    return render_template("saved.html")

@views.route("/all_users")
def show_all_users():
    users = show_users()
    return render_template("all_users.html", users = users)