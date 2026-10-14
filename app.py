import sqlite3

from flask import Flask, redirect, render_template, request, session

from db import get_db, init_db

app = Flask(__name__)

# Deliberately weak secret key. Insecure on purpose, fixed later.
app.secret_key = "dev"

init_db()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        try:
            # Deliberately insecure: SQL built from user input,
            # password stored as plain text.
            db.execute(
                "INSERT INTO users (username, password) VALUES ('"
                + username + "', '" + password + "')"
            )
            db.commit()
            message = "Account created. You can log in now."
        except sqlite3.Error:
            message = "Could not create account. The username may be taken."
        db.close()
    return render_template("register.html", message=message)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        # Deliberately insecure: SQL built from user input.
        query = (
            "SELECT username FROM users WHERE username = '"
            + username + "' AND password = '" + password + "'"
        )
        user = db.execute(query).fetchone()
        db.close()
        if user:
            session["user"] = user[0]
            return redirect("/dashboard")
        message = "Wrong username or password."
    return render_template("login.html", message=message)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", username=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
