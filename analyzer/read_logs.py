"""Reads logs/app.log, summarises events, and flags suspicious patterns."""

from collections import Counter, defaultdict
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "app.log"

BRUTE_FORCE_THRESHOLD = 5   # failed logins for one username = suspicious
SQLI_MARKERS = ["'", "--", " or ", "=1", "1=1"]
XSS_MARKERS = ["<script", "onerror=", "javascript:"]


def read_log_lines():
    if not LOG_FILE.exists():
        print("No log file found yet.")
        return []
    with open(LOG_FILE) as f:
        return f.readlines()


def parse_line(line):
    """Pulls event and username out of one log line, if present."""
    event = None
    username = None
    if "event=" in line:
        event = line.split("event=")[1].split()[0]
    if 'username="' in line:
        username = line.split('username="')[1].split('"')[0]
    return event, username


def summarise(lines):
    event_counts = Counter()
    for line in lines:
        event, _ = parse_line(line)
        if event:
            event_counts[event] += 1
    return event_counts


def detect_brute_force(lines):
    """Flags any username with repeated login_failed events."""
    failed_per_user = defaultdict(int)
    for line in lines:
        event, username = parse_line(line)
        if event == "login_failed" and username:
            failed_per_user[username] += 1

    alerts = []
    for username, count in failed_per_user.items():
        if count >= BRUTE_FORCE_THRESHOLD:
            alerts.append(
                f"Possible brute force: '{username}' failed login {count} times"
            )
    return alerts


def detect_injection_attempts(lines):
    """Flags usernames that look like SQL injection or XSS payloads."""
    alerts = []
    seen = set()
    for line in lines:
        _, username = parse_line(line)
        if not username or username in seen:
            continue
        lowered = username.lower()
        if any(marker in lowered for marker in SQLI_MARKERS):
            alerts.append(f"Possible SQL injection attempt in username: {username}")
            seen.add(username)
        elif any(marker in lowered for marker in XSS_MARKERS):
            alerts.append(f"Possible XSS attempt in username: {username}")
            seen.add(username)
    return alerts


if __name__ == "__main__":
    lines = read_log_lines()
    counts = summarise(lines)

    print(f"Total log lines: {len(lines)}")
    print("Event counts:")
    for event, count in counts.most_common():
        print(f"  {event}: {count}")

    print("\nAlerts:")
    alerts = detect_brute_force(lines) + detect_injection_attempts(lines)
    if alerts:
        for alert in alerts:
            print(f"  ⚠ {alert}")
    else:
        print("  None")