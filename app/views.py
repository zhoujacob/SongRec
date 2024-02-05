from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user 
from .api import get_token, get_song

views = Blueprint("views", __name__)

# Reference current user to see if it is authenticated
@views.route("/", methods = ["GET", "POST"])
@views.route("/home", methods=["GET", "POST"])
@login_required
def home():
    songs = None
    selected_song = None

    if request.method == 'POST':
        # Check if the search form is submitted
        if 'search-bar' in request.form:
            song_name = request.form['search-bar']
            token = get_token()
            songs = get_song(token, song_name)

        # Check if a song is selected
        elif 'selected_song' in request.form:
            selected_song = request.form['selected_song']

        return render_template('home.html', user=current_user, songs=songs, selected_song = selected_song) 
    return render_template("home.html", user = current_user)

    
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
