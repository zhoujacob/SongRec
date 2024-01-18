from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello! this is the home page, this page will also ask what song you want to find recommendations for"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route("/recent")
def recent_sh():
    return "Recent Search History will be displayed here"

@app.route("/saved")
def saved_songs():
    return "Saved songs will be displayed here"

if __name__ == "__main__":
    app.run()