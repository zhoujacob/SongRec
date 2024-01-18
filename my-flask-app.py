from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("show_user_profile", username = user))
    else:
        return render_template("login.html")
    
@app.route("/<username>")
def show_user_profile(username):
    return render_template("user.html", user = username)

@app.route("/history")
def search_history():
    return render_template("search_history.html")

@app.route("/saved")
def saved_songs():
    return render_template("saved.html")

if __name__ == "__main__":
    app.run()