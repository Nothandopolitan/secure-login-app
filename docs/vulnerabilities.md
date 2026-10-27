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
- Date: 16 Oct 2026
- Where: /login
- Payload: username = demo' -- , password = anything
- Result: Logged in as demo with no correct password. Server returned 302 to /dashboard.
- Why it works: app.py builds the SQL query by joining the input directly into the query string, instead of using placeholders. The -- starts a SQL comment, so everything after it, including the password check, is ignored.
- Log evidence: logs/app.log shows login_success for username="demo' -- ", proving a login happened without a real password check.
- Planned fix: use parameterised queries (db.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)))

## Attack 2: Stored XSS (Dashboard)
- Date: 26 Oct 2026
- Where: /register and /dashboard
- Setup: dashboard.html uses {{ username | safe }}, turning off Jinja2's automatic escaping (deliberate, documented in insecure-design-notes.md)
- Payload: username = <script>alert("XSS")</script>, password = 1234
- First attempt used single quotes (alert('XSS')) and failed, because the quote broke the SQL insert statement (same bug as Attack 1). Log shows register_failed.
- Second attempt with double quotes succeeded. Log shows register_success, then login_success.
- Result: visiting /dashboard ran the script instead of printing it as text. A popup alert box appeared showing "XSS".
- Log evidence (logs/app.log):
  - 2026-10-26 14:36:07 WARNING register_failed username="<script>alert('XSS')</script>"
  - 2026-10-26 14:36:49 INFO register_success username="<script>alert("XSS")</script>"
  - 2026-10-26 14:37:23 INFO login_success username="<script>alert("XSS")</script>"
- Why it works: the | safe filter tells Jinja2 not to escape the username, so any HTML or script in it runs as real code in the browser.
- Planned fix: remove | safe so Jinja2 escapes the username normally (already documented as the fix in insecure-design-notes.md)

## Attack 3: Brute Force (No Rate Limiting)
- Where: /login
- Method: sent 10 login attempts in a row for username "demo" with different wrong passwords, no delay between attempts
- Result: all 10 attempts were accepted and processed normally. No lockout, no delay, no CAPTCHA.
- Log evidence: logs/app.log shows 10 login_failed lines in a row, all for username="demo", seconds apart
- Why it works: /login has no limit on how many times a password can be guessed
- Planned fix: add rate limiting (e.g. lock the account or slow down attempts after a few failures)
