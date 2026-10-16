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