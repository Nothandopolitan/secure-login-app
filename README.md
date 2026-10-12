# Secure Login App with Attack Detection

## 1. Overview
A small Flask web app that I build, attack, monitor and then fix. The goal is to learn practical cybersecurity by doing both offence and defence, and to document every step with evidence.

**Ethics note:** I only attack my own app, running in my own environment. Nothing here is aimed at anyone else's system.

## 2. Goals
- Build a working login and registration system
- Find real vulnerabilities by attacking it myself
- Build a log analyzer that detects those attacks
- Fix every weakness and prove the fix works
- Show daily progress through commits and a daily log

## 3. Tech stack
- Python and Flask (web app)
- SQLite (database)
- HTML templates (Jinja2)
- GitHub Codespaces (coding in the browser, no computer needed)
- Git and GitHub (version control and proof of daily work)

## 4. Features
**The app:** registration, login, logout, a profile page, a protected dashboard.
**Logging:** every login attempt (success or fail), registration, error and suspicious input, with time, IP and username.
**Analyzer:** reads the log file and raises alerts.
**Alerts page:** shows what the analyzer found.

## 5. Attacks I will test (OWASP Top 10 based)
1. SQL injection on the login form
2. Cross-site scripting (XSS) in a profile or comment field
3. Brute-force password guessing
4. Weak passwords and plain-text password storage
5. Broken session handling (staying logged in after logout)
6. Broken access control (viewing pages I should not see)

## 6. Detection rules
- 5+ failed logins from one IP within 5 minutes = brute-force alert
- Quotes, OR 1=1 or -- in a username field = SQL injection alert
- script tags in any input = XSS alert
- Many different usernames tried from one IP = credential stuffing alert
- Login at unusual hours = low-level warning

## 7. Fixes I will apply
- Parameterised queries (stops SQL injection)
- Escape output and validate input (stops XSS)
- Hash passwords with bcrypt or Werkzeug
- Rate limiting and temporary lockout
- Secure session cookies and proper logout
- Login-required checks on protected pages
- Minimum password rules
