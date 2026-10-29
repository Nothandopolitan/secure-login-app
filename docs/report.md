# Secure Login App with Attack Detection — Final Report

## 1. Executive Summary

This project involved building, attacking, monitoring, and securing a Flask web application utilizing an SQLite database. The core objective was to apply offensive cybersecurity techniques to identify OWASP Top 10 vulnerabilities in a controlled environment, observe their presence in logs and network captures, implement robust security controls, and verify that all weaknesses were mitigated.

All **10 OWASP Top 10** targeted vulnerabilities were successfully identified, patched, and verified through automated terminal commands (`curl`, `sqlite3`, and `safety`).

---

## 2. Architecture & Tech Stack

* **Framework:** Flask (Python 3.14)
* **Database:** SQLite3 (`users.db`)
* **Authentication & Hashing:** Werkzeug Security (`generate_password_hash`, `check_password_hash` using `scrypt`)
* **Logging & Monitoring:** Custom Python log helper (`app_logging.py`), custom log analyzer, Scapy network sniffer
* **Dependency Auditing:** `safety` CLI
* **Environment:** GitHub Codespaces / Linux

---

## 3. Comprehensive OWASP Top 10 Defense Matrix

| OWASP Category | Vulnerability Description | Defensive Fix Implemented in `app.py` | Verification & Retest Result |
| :--- | :--- | :--- | :--- |
| **A01: Broken Access Control** | Unauthenticated users could access protected routes like `/users`, `/dashboard`, `/import-settings`, and `/fetch-external`. | Implemented custom `@login_required` Python decorator returning server-side `302 FOUND` redirects to `/login`. | **PASSED:** `curl -i http://127.0.0.1:5000/users` returned `HTTP/1.1 302 FOUND` pointing to `/login`. |
| **A02: Cryptographic Failures** | User credentials were stored as plain text in the SQLite database (`users.db`). | Integrated Werkzeug `generate_password_hash()` using cryptographic `scrypt` key derivation. | **PASSED:** Database query verified hashes (`scrypt:32768:8:1$...`) replacing cleartext strings. |
| **A03: Injection (SQLi & XSS)** | Raw SQL concatenation allowed authentication bypass (`demo' --`), and unsanitized inputs allowed XSS execution. | Converted database queries to parameterized prepared statements (`?`) and enforced Jinja2 HTML auto-escaping. | **PASSED:** SQLi payload returned `HTTP/1.1 200 OK` with "Wrong username or password" (no bypass). |
| **A04: Insecure Design** | Unlimited login attempts enabled automated brute-force credential guessing. | Implemented in-memory rate limiting and account lockout (`FAILED_LOGIN_LIMIT = 5`, `LOCKOUT_SECONDS = 60`). | **PASSED:** 6th attempt triggered account lockout with a `"login_blocked"` event logged. |
| **A05: Security Misconfiguration** | Debug mode and default exception handlers exposed internal Python stack traces to users. | Set `debug=False` and registered custom `@app.errorhandler(500)` and `404` handlers. | **PASSED:** System returned clean, generic error responses without exposing tracebacks or internal paths. |
| **A06: Vulnerable Components** | Third-party dependencies could contain known CVE security vulnerabilities. | Conducted environment-wide vulnerability scanning across all installed Python packages using `safety`. | **PASSED:** `safety scan` reported **0 vulnerabilities** across 132 scanned Python packages. |
| **A07: Authentication Failures** | User session state persisted post-logout, allowing session reuse. | Implemented complete server-side session purging via `session.clear()` inside `/logout`. | **PASSED:** `/logout` successfully cleared session tokens and redirected to home (`/`). |
| **A08: Software & Data Integrity** | Deserializing untrusted objects (e.g., Python `pickle`) creates remote code execution risks. | Built safe JSON endpoint (`/import-settings`) utilizing strict `request.get_json()` structure validation. | **PASSED:** Authenticated POST returned `200 OK` with `{"status":"Settings updated safely"}`. |
| **A09: Logging & Monitoring Failures** | Lack of security log visibility prevents early breach and attack detection. | Built structured audit logger (`app_logging.py`) and log analyzer scanning for brute-force and injection signatures. | **PASSED:** All events (`login_failed`, `access_denied`, `ssrf_attempt_blocked`) recorded in `logs/app.log`. |
| **A10: Server-Side Request Forgery (SSRF)** | Unvalidated external requests allow attackers to target internal IP ranges (`169.254.169.254`). | Built URL destination filtering (`/fetch-external`) using `urlparse` against an `ALLOWED_DOMAINS` whitelist. | **PASSED:** Targeting AWS metadata IP returned `HTTP/1.1 403 FORBIDDEN` (`"Access to targeted URL is forbidden"`). |

---

## 4. Monitoring & Attack Detection

* **Application Logger (`app_logging.py`):** Captures structured events (`register_success`, `login_failed`, `login_blocked`, `access_denied`, `ssrf_attempt_blocked`) with ISO timestamps, source IP, and username.
* **Log Analyzer:** Reads `logs/app.log` and flags suspicious patterns (5+ failed logins within 5 minutes or SQL injection keywords) to populate real-time security alerts.
* **Packet Sniffer:** Inspects raw HTTP network traffic on port 5000 using Scapy to detect unencrypted payloads at the network level.

---

## 5. Summary of Terminal Retest Commands & Evidence

```bash
# 1. Access Control (A01)
curl -i [http://127.0.0.1:5000/users](http://127.0.0.1:5000/users)
# Result: HTTP/1.1 302 FOUND (Location: /login)

# 2. Cryptographic Password Hashing (A02)
python3 -c "import sqlite3; c=sqlite3.connect('users.db').execute('SELECT * FROM users'); print([d[0] for d in c.description]); [print(r) for r in c.fetchall()]"
# Result: (1, 'demo', 'scrypt:32768:8:1$...')

# 3. SQL Injection (A03)
curl -i -X POST [http://127.0.0.1:5000/login](http://127.0.0.1:5000/login) -d "username=demo' --&password=anything"
# Result: HTTP/1.1 200 OK ("Wrong username or password.")

# 4. Vulnerable Dependencies Scan (A06)
safety check
# Result: 0 vulnerabilities reported across 132 packages

# 5. Authenticated Data Integrity (A08)
curl -i -b cookie.txt -X POST [http://127.0.0.1:5000/import-settings](http://127.0.0.1:5000/import-settings) -H "Content-Type: application/json" -d '{"theme": "dark"}'
# Result: HTTP/1.1 200 OK ("Settings updated safely")

# 6. Authenticated SSRF Block (A10)
curl -i -b cookie.txt -X POST [http://127.0.0.1:5000/fetch-external](http://127.0.0.1:5000/fetch-external) -d "url=[http://169.254.169.254/latest/meta-data/](http://169.254.169.254/latest/meta-data/)"
# Result: HTTP/1.1 403 FORBIDDEN ("Access to targeted URL is forbidden")
