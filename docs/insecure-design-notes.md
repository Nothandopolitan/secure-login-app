# Deliberate Weaknesses (version 1)

This version is insecure on purpose. Each weakness below is attacked, documented and fixed later.

| Weakness | Where | Planned attack | Planned fix |
|---|---|---|---|
| SQL built from user input | /login and /register | SQL injection | Parameterised queries |
| Dashboard shows username with auto-escaping turned off (`\| safe`) | /dashboard | Stored XSS | Remove `\| safe`, let Jinja2 escape normally |
| Passwords stored as plain text | users table | Read the database | Hash with Werkzeug or bcrypt |
| No limit on login attempts | /login | Brute force | Rate limiting and lockout |
| Weak secret key ("dev") | app.py | Forge a session | Long random key from the environment |
| No password rules | /register | Weak passwords accepted | Minimum password rules |
| Session is only checked in one place | /dashboard | Broken access control | Reusable login-required check |

To run the app: `python3 -m flask --app app run --host=0.0.0.0 --port 5000`
