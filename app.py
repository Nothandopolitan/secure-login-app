import os
import secrets
import sqlite3
import time
import json
from urllib.parse import urlparse
from functools import wraps

from flask import Flask, redirect, render_template, request, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db, init_db
from app_logging import log_event

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

init_db()

FAILED_LOGIN_LIMIT = 5
LOCKOUT_SECONDS = 60
login_attempts = {}

# Allowed domains for SSRF Protection (A10:2021)
ALLOWED_DOMAINS = ["api.github.com", "httpbin.org"]


def is_locked_out(username):
    record = login_attempts.get(username)
    if not record:
        return False
    return record["count"] >= FAILED_LOGIN_LIMIT and time.time() < record["locked_until"]


def record_failed_login(username):
    record = login_attempts.setdefault(username, {"count": 0, "locked_until": 0})
    record["count"] += 1
    if record["count"] >= FAILED_LOGIN_LIMIT:
        record["locked_until"] = time.time() + LOCKOUT_SECONDS


def reset_failed_login(username):
    login_attempts.pop(username, None)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user" not in session:
            log_event("access_denied", level="warning")
            return redirect("/login")
        return view(*args, **kwargs)
    return wrapped


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed = generate_password_hash(password)
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed),
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
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if is_locked_out(username):
            log_event("login_blocked", username, "warning")
            message = "Too many failed attempts. Try again in a minute."
            return render_template("login.html", message=message)

        db = get_db()
        row = db.execute(
            "SELECT username, password FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        db.close()

        if row and check_password_hash(row[1], password):
            session["user"] = row[0]
            reset_failed_login(username)
            log_event("login_success", username)
            return redirect("/dashboard")

        record_failed_login(username)
        log_event("login_failed", username, "warning")
        message = "Wrong username or password."
    return render_template("login.html", message=message)


@app.route("/dashboard")
@login_required
def dashboard():
    log_event("dashboard_access", session["user"])
    return render_template("dashboard.html", username=session["user"])


@app.route("/users")
@login_required
def list_users():
    log_event("users_access", session["user"])
    db = get_db()
    rows = db.execute("SELECT username FROM users").fetchall()
    db.close()
    return "<br>".join(row[0] for row in rows)


# --- OWASP A08: Software and Data Integrity Failures Fix ---
# Safe Data Import via JSON instead of unsafe Python pickle deserialization
@app.route("/import-settings", methods=["POST"])
@login_required
def import_settings():
    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON format"}), 400
        log_event("settings_imported", session["user"])
        return jsonify({"status": "Settings updated safely", "data": data})
    except Exception:
        log_event("settings_import_failed", session["user"], "warning")
        return jsonify({"error": "Failed to parse data"}), 400


# --- OWASP A10: Server-Side Request Forgery (SSRF) Fix ---
# Destination Whitelisting Control for external API requests
@app.route("/fetch-external", methods=["POST"])
@login_required
def fetch_external():
    target_url = request.form.get("url", "")
    parsed = urlparse(target_url)

    # Validate scheme and domain against whitelist
    if parsed.scheme not in ["http", "https"] or parsed.netloc not in ALLOWED_DOMAINS:
        log_event("ssrf_attempt_blocked", session["user"], "warning")
        return jsonify({"error": "Access to targeted URL is forbidden"}), 403

    log_event("external_fetch_success", session["user"])
    return jsonify({"status": "Destination validated and permitted", "url": target_url})


@app.route("/logout")
def logout():
    log_event("logout", session.get("user", "-"))
    session.clear()
    return redirect("/")


# --- OWASP A05: Security Misconfiguration Handlers ---
@app.errorhandler(sqlite3.Error)
def handle_database_error(error):
    log_event("database_error", request.form.get("username", "-"), "error")
    return "Something went wrong.", 500


@app.errorhandler(500)
def handle_internal_error(error):
    log_event("internal_server_error", level="error")
    return "An internal server error occurred. Please try again later.", 500


@app.errorhandler(404)
def handle_not_found(error):
    return "Page not found.", 404


if __name__ == "__main__":
    app.run(port=5000, debug=False)
