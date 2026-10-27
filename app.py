import sqlite3

from flask import Flask, redirect, render_template, request, session

from db import get_db, init_db
from app_logging import log_event

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
            db.execute(
                "INSERT INTO users (username, password) VALUES ('"
                + username + "', '" + password + "')"
            )
            db.commit()
            message = "Account created. You can log in now."
            log_event("register_success", username)
        except sqlite3.Error:
            message = "Could not create account. The username may be taken."
            log_event("register_failed", username, "warning")
        db.close()
    return render_template("register.html", message=message)

@app.route("/login", methods=["GET", "POST"])
def login():
    mes
