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
- Scapy (Python library for capturing and reading packets)

## 4. Features
**The app:** registration, login, logout, a profile page, a protected dashboard.
**Logging:** every login attempt (success or fail), registration, error and suspicious input, with time, IP and username.
**Analyzer:** reads the log file and raises alerts.
**Packet sniffer:** watches network traffic to my own app and flags suspicious patterns (see section 7).
**Alerts page:** shows what the analyzer and the sniffer found.

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

## 7. Packet sniffer (network monitor)
A small Python tool using Scapy that watches the network traffic going to my own Flask app while it runs in my own environment (localhost only) and flags suspicious patterns. This lets me see attacks at the network level as well as in the app logs.

**What it does:**
- Captures packets on the port the app runs on (e.g. 5000)
- Records time, source IP, destination port and request path
- Writes alerts to logs/network-alerts.log and shows them on the alerts page

**Network detection rules:**
- 20+ requests to the login page from one IP within 1 minute = network brute-force alert
- Quotes or SQL keywords in request data = network SQL injection alert
- script tags in request data = network XSS alert
- One IP connecting to many ports = port scan alert (stretch goal)

**Ethics:** it only captures traffic to my own app in my own environment. I do not capture anyone else's traffic.

**Limitations:** it needs admin rights to run, and it cannot read encrypted (HTTPS) traffic, so I test the app over plain HTTP locally. If it will not run in Codespaces, I will log raw requests inside Flask instead.

## 8. Fixes I will apply
- Parameterised queries (stops SQL injection)
- Escape output and validate input (stops XSS)
- Hash passwords with bcrypt or Werkzeug
- Rate limiting and temporary lockout
- Secure session cookies and proper logout
- Login-required checks on protected pages
- Minimum password rules

## 9. Day-by-day timeline
| Date | Task |
|---|---|
| Mon 12 Oct | Create repo, README, daily log |
| Tue 13 Oct | Set up Codespaces, run a Flask "Hello World" |
| Wed 14 Oct | Build registration and login with SQLite (deliberately insecure) |
| Thu 15 Oct | Add logging to a log file |
| Fri 16 Oct | Attack 1: SQL injection, document it |
| Sat 17 Oct | Attack 2: XSS, document it |
| Sun 18 Oct | Attack 3: brute force with a simple script, document it |
| Mon 19 Oct | Attack 4: weak and plain-text passwords |
| Tue 20 Oct | Attacks 5 and 6: sessions and access control |
| Wed 21 Oct | Analyzer: read and parse the log file |
| Thu 22 Oct | Analyzer: add the detection rules |
| Fri 23 Oct | Packet sniffer: capture traffic to my own app and flag attack patterns |
| Sat 24 Oct | Alerts page for log and sniffer alerts, test against my attacks |
| Sun 25 Oct | Fix SQL injection, XSS and passwords, add rate limiting, retest |
| Mon 26 Oct | Fix sessions and access control, full retest |
| Tue 27 Oct | Write the final report |
| Wed 28 Oct | Polish README, record demo, submit |

## 10. Daily routine
1. Work on that day's task
2. Commit with a clear message (e.g. "Add SQL injection test")
3. Add an entry to docs/daily-log.md (what I did, what I learned, what is next)
4. Save screenshots in docs/screenshots/

## 11. Documentation
- docs/daily-log.md: daily progress
- docs/vulnerabilities.md: one section per attack (attack, steps, evidence, what the monitor caught, fix, retest result)
- docs/report.md: final report with before and after results

## 12. Repo structure
- README.md
- app.py
- templates/
- logs/
- analyzer/
- sniffer/
- attacks/
- docs/ (daily-log.md, vulnerabilities.md, report.md, screenshots/)

## 13. What I need to learn
- Flask basics (routes, forms, templates)
- SQL basics (SELECT, INSERT)
- How SQL injection, XSS and brute force work
- Reading and parsing text files in Python
- Basics of network packets and how Scapy captures them
- Git basics (commit, push)

## 14. Final deliverables
- Working app (insecure version and secure version)
- Log analyzer with alerts page
- Packet sniffer that flags suspicious traffic to my own app
- Full documentation and final report
- Short demo video
