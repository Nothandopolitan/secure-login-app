## Detection rules (read_logs.py)

The analyzer reads logs/app.log and flags two kinds of suspicious activity:

- **Brute force**: a username with 5 or more login_failed events
- **Injection attempts**: a username containing SQL injection markers (quotes, --, OR, =1) or XSS markers (<script, onerror=, javascript:)

Tested against the real attack logs from Attacks 1, 2 and 3. It correctly flagged the SQL injection usernames used in Attack 1 (demo' --) and the brute force attempt from Attack 3.

Known limitation: it checks for exact substrings, so an attacker could use different injection syntax to avoid detection. This is a basic rule-based detector, not a full intrusion detection system.