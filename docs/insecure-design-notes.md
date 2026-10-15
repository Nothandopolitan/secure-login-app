# Deliberate Weaknesses (version 1)

This version is insecure on purpose. Each weakness below is attacked, documented and fixed later.

| Weakness | Where | Planned attack | Planned fix |
|---|---|---|---|
| SQL built from user input | /login and /register | SQL injection | Parameterised queries |
| Passwords stored as plain text | users table | Read the database | Hash with Werkzeug or bcrypt |
| No limit on login attempts | /login | Brute force | Rate limiting and lockout |
| Weak secret key ("dev") | app.py | Forge a session | Long random key from the environment |
| No password rules | /register | Weak passwords accepted | Minimum password rules |
| Session is only checked in one place | /dashboard | Broken access control | Reusable login-required check |

To run the app: `FLASK_APP=app python3 -m flask run --port 5000`
