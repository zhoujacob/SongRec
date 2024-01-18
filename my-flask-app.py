from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return render_template("user.html", user = username)

@app.route("/history")
def search_history():
    return render_template("search_history.html")

@app.route("/saved")
def saved_songs():
    return render_template("saved.html")

if __name__ == "__main__":
    app.run()