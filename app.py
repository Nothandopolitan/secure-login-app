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
