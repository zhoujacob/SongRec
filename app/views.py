from flask import Blueprint, render_template, request, flash, redirect, url_for, json
from flask_login import login_required, current_user 
from .api import get_token, get_song, get_recommendations
from .models import Saved, get_db_connection
from . import db

views = Blueprint("views", __name__)

# Reference current user to see if it is authenticated
@views.route("/", methods = ["GET", "POST"])
@views.route("/home", methods=["GET", "POST"])
@login_required
def home():
    songs = None
    selected_song = request.args.get('selected_song_details')

    if request.method == 'POST':
        # Handle the search form
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

    # Goes back to home page with selected song
    return redirect(url_for('views.home', user=current_user, selected_song_details=selected_song_details))

@views.route("/recommendations", methods=["GET", "POST"])
@login_required
def recommendations():
    if request.method == "POST":
        # to propert JSON Format
        selected_song_details_json = request.form['selected_song_details'].replace("'", '"')
        # Converts JSON string to a Python Dictionary
        selected_song_details = json.loads(selected_song_details_json)

        if selected_song_details:
            token = get_token()

            seed_artist = selected_song_details['artist_uri']
            seed_track = selected_song_details['id']

            rec = get_recommendations(token, seed_artist, seed_track)
            if rec is None:
                flash("No recommendations available for this song.")
                return redirect(url_for('views.home'))
            
            return render_template('recommendations.html', user = current_user, recommendations = rec)

        return redirect(url_for('views.home'))
    return render_template("recommendations.html", user = current_user)
    
@views.route("/save_song", methods=["POST"])
@login_required
def save_song():
    if request.method == 'POST':
        saved_song_details_json = request.form['saved_song_details'].replace("'", '"')
        saved_song_details = json.loads(saved_song_details_json)
        
        if saved_song_details:
            song_name = saved_song_details['name']
            artist_name = saved_song_details['artist']

            new_saved_song = Saved(song=song_name, artist=artist_name, user_id=current_user.id)
            db.session.add(new_saved_song)
            db.session.commit()
            flash('Song Added!', category='success')
    # Goes back to home page with selected song
    return redirect(url_for('views.recommendations', user = current_user))


@views.route("/history")
@login_required
def history():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Saved;')
    savedsongs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("saved.html", user =current_user, savedsongs = savedsongs)
