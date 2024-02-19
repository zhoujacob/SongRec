from flask_wtf.csrf import generate_csrf
from flask import Blueprint, render_template, request, flash, redirect, url_for, json, render_template_string
from flask_login import login_required, current_user 
from .api import get_token, get_song, get_recommendations
from .models import Saved, get_db_connection
from . import db
import json

views = Blueprint("views", __name__)

# Reference current user to see if it is authenticated
@views.route("/", methods = ["GET", "POST"])
@views.route("/home", methods=["GET", "POST"])
@login_required
def home():
    songs = None
    selected_song_details = None

    if(request.args.get('selected_song_details')):
        submit = True
        selected_song = request.args.get('selected_song_details').replace("'", '"')
        selected_song_details = json.loads(selected_song)
    else:
        submit = False

    if request.method == 'POST':
        # Handle the search form
        submit = True
        if 'search-bar' in request.form:
            song_name = request.form['search-bar']
            token = get_token()
            songs = get_song(token, song_name)
    
    return render_template('home.html', user=current_user, songs=songs, selected_song=selected_song_details, submit = submit)

@views.route("/select_song", methods=["POST"])
@login_required
def select_song():
    selected_song_id = request.form['selected_song']
    token = get_token()
    selected_song_details = get_song(token, selected_song_id)
    submit = True

    # Goes back to home page with selected song
    return redirect(url_for('views.home', user=current_user, selected_song_details=selected_song_details, submit = submit))

@views.route("/recommendations", methods=["GET", "POST"])
@login_required
def recommendations():
    if request.method == "POST":
        # to proper JSON Format
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
            
            # Generate CSRF token
            csrf_token = generate_csrf()

            return render_template('recommendations.html', user=current_user, recommendations=rec, csrf_token=csrf_token)

        return redirect(url_for('views.home'))
    return render_template("recommendations.html", user=current_user)
    
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


@views.route("/remove_song", methods=["POST"])
@login_required
def remove_song():
    if request.method == 'POST':
        song_id = request.form['song_id']
        if song_id:
            song_to_remove = Saved.query.get(song_id)
            if song_to_remove:
                db.session.delete(song_to_remove)
                db.session.commit()
                flash('Song Removed Successfully', category = 'success')
            else:
                flash('Song Not Removed', category = 'error')
        else:
            flash('No song ID provided.', category = 'error')
    return redirect(url_for('views.history', user = current_user))

@views.route("/history", methods=["GET"])
@login_required
def history():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM Saved WHERE user_id = %s;', (current_user.id,))
    savedsongs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("history.html", user =current_user, savedsongs = savedsongs)
