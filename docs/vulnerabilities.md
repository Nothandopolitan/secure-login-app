# Vulnerabilities

One section per attack. Copy this template for each one.

## Attack name
- **Attack:** what type of attack it is
- **How I did it:** the exact input or steps
- **Evidence:** screenshot or log line
- **What the monitor caught:** the alert from the analyzer or sniffer
- **The fix:** what I changed in the code
- **Retest result:** blocked or not

## Attack 1: SQL Injection (Login Bypass)
- Where: /login
- Payload: username = demo' -- , password = anything
- Result: Logged in as demo with no correct password. Server returned 302 to /dashboard.
- Why it works: app.py builds the SQL query by joining the input directly into the query string, instead of using placeholders. The -- starts a SQL comment, so everything after it, including the password check, is ignored.
- Log evidence: logs/app.log shows login_success for username="demo' -- ", proving a login happened without a real password check.
- Planned fix: use parameterised queries (db.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)))

## Attack 2: Stored XSS (Dashboard)
- Where: /register and /dashboard
- Setup: dashboard.html uses {{ username | safe }}, turning off Jinja2's automatic escaping (deliberate, documented in insecure-design-notes.md)
- Payload: username = <script>alert("XSS")</script>, password = 1234
- First attempt used single quotes (alert('XSS')) and failed, because the quote broke the SQL insert statement (same bug as Attack 1). Log shows register_failed.
- Second attempt with double quotes succeeded. Log shows register_success, then login_success.
- Result: visiting /dashboard ran the script instead of printing it as text. A popup alert box appeared showing "XSS".
- Log evidence (logs/app.log):
  - WARNING register_failed username="<script>alert('XSS')</script>"
  - INFO register_success username="<script>alert("XSS")</script>"
  - INFO login_success username="<script>alert("XSS")</script>"
- Why it works: the | safe filter tells Jinja2 not to escape the username, so any HTML or script in it runs as real code in the browser.
- Planned fix: remove | safe so Jinja2 escapes the username normally (already documented as the fix in insecure-design-notes.md)

## Attack 3: Brute Force (No Rate Limiting)
- Where: /login
- Method: sent 10 login attempts in a row for username "demo" with different wrong passwords, no delay between attempts
- Result: all 10 attempts were accepted and processed normally. No lockout, no delay, no CAPTCHA.
- Log evidence: logs/app.log shows 10 login_failed lines in a row, all for username="demo", seconds apart
- Why it works: /login has no limit on how many times a password can be guessed
- Planned fix: add rate limiting (e.g. lock the account or slow down attempts after a few failures)

## Attack 4: Plaintext Password Storage
- Where: users table in users.db
- Method: registered a user (demo / mypassword123), then queried the database directly: SELECT username, password FROM users
- Result: the password came back exactly as typed: [('demo', 'mypassword123')]
- Why it works: db.py stores the password string directly with no hashing
- Planned fix: hash passwords before storing (e.g. with Werkzeug's generate_password_hash) and compare hashes on login instead of comparing raw strings

## Attack 5: Session Forgery (Weak Secret Key)
- Where: session cookie, signed using app.secret_key
- Setup: app.py sets app.secret_key = "dev", a weak hardcoded key
- Method: used flask-unsign to sign a fake session cookie claiming {'user': 'admin'}, using the known key "dev", with no registration or login at all
- Result: sending that forged cookie to /dashboard returned 200 OK and showed "Welcome, admin." No account named admin was ever created or logged into.
- Extra finding: the forged, successful dashboard visit left no log entry at all. The log only records dashboard_denied (failed) visits, never successful ones, so this attack is invisible in the current logging.
- Why it works: Flask trusts any cookie correctly signed with secret_key. A weak, guessable key lets anyone forge a valid session for any username.
- Planned fix: use a long, random secret_key loaded from an environment variable, not hardcoded in the source code. Also add a log line for successful dashboard access, not just denied access.

## Attack 6: Broken Access Control
- Where: /users (a new route, not previously in the app)
- Setup: /dashboard checks "if 'user' not in session" before showing content. /users was added without that same check, since the login check isn't reusable and has to be copy-pasted into every protected route.
- Method: visited /users directly with curl, no login, no session, no cookie at all
- Result: the route returned the username(s) in the database with full access, no authentication required
- Log evidence: logs/app.log has no entry at all for this access, since the route never calls log_event. The attack is completely invisible.
- Why it works: access control is only applied per-route, by hand, instead of being enforced in one reusable place. Forgetting to add the check (as this route demonstrates) leaves it wide open.
- Planned fix: write one reusable "login_required" check (a decorator) and apply it to every route that needs protection, so a forgotten check like this can't happen. Also log every dashboard/users access, not just denied ones.
