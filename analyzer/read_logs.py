"""Reads logs/app.log and prints a summary of events."""

from collections import Counter
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "app.log"


def read_log_lines():
    if not LOG_FILE.exists():
        print("No log file found yet.")
        return []
    with open(LOG_FILE) as f:
        return f.readlines()


def summarise(lines):
    event_counts = Counter()
    for line in lines:
        if "event=" in line:
            # pull out the word right after event=
            part = line.split("event=")[1]
            event_name = part.split()[0]
            event_counts[event_name] += 1
    return event_counts


if __name__ == "__main__":
    lines = read_log_lines()
    counts = summarise(lines)
    print(f"Total log lines: {len(lines)}")
    print("Event counts:")
    for event, count in counts.most_common():
        print(f"  {event}: {count}")
