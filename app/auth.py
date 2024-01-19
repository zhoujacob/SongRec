from flask import Blueprint, render_template, request, redirect, url_for

auth = Blueprint("auth", __name__)

@auth.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["usernameID"]
        return redirect(url_for("show_user_profile", username = user))
    else:
        return render_template("login.html", boolean = True)
    
@auth.route("/logout")
def logout():
    return "<p>Logout</p>"

@auth.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")
    