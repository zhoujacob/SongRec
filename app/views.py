from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user 
from .api import get_token, get_song, get_recommendations

views = Blueprint("views", __name__)

# Reference current user to see if it is authenticated
@views.route("/", methods = ["GET", "POST"])
@views.route("/home", methods=["GET", "POST"])
@login_required
def home():
    songs = None
    selected_song = request.args.get('selected_song_details')

    if request.method == 'POST':
        # Handle the search form as before
        if 'search-bar' in request.form:
            song_name = request.form['search-bar']
            token = get_token()
            songs = get_song(token, song_name)

    return render_template('home.html', user=current_user, songs=songs, selected_song=selected_song)

@views.route("/select_song", methods=["POST"])
@login_required
def select_song():
    selected_song_id = request.form['selected_song']
    token = get_token()
    selected_song_details = get_song(token, selected_song_id)

    return redirect(url_for('views.home', user=current_user, selected_song_details=selected_song_details))

@views.route("/recommendations", methods = ["GET", "POST"])
@login_required
def recommendations():
    # selected_song_details = request.form.get['selected_song_details']
    # token = get_token()

    # seed_artist = selected_song_details.get('artist')
    # seed_track = selected_song_details.get('id')

    # rec = get_recommendations(token, seed_artist, seed_track)
    
    return render_template('recommendations.html', user = current_user)

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
