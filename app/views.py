from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user 
# from . import get_token, get_auth_header

views = Blueprint("views", __name__)

# Reference current user to see if it is authenticated
@views.route("/")
@views.route("/home", methods=["GET", "POST"])
@login_required
def home():
    if request.method == 'POST':
        song = request.form['search-bar']
        # token = get_token()
        # auth_header = get_auth_header(token)
        # recommendations = get_recommendations(auth_header)
        return render_template('home.html',user = current_user, song = song)
    return render_template("home.html", user = current_user)

# @views.route("/search")
# def search():

    
@views.route("/<username>")
@login_required
def show_user_profile(username):
    return render_template("user.html", user = username)

@views.route("/history")
@login_required
def search_history():
    return render_template("search_history.html", user = current_user)

@views.route("/saved")
@login_required
def saved_songs():
    return render_template("saved.html", user = current_user)
