"""Writes security events to logs/app.log in a format the analyzer can read."""

import logging
from pathlib import Path

from flask import request

LOG_FILE = Path(__file__).resolve().parent / "logs" / "app.log"

_logger = logging.getLogger("secure_login_app")
_logger.setLevel(logging.INFO)

if not _logger.handlers:
    LOG_FILE.parent.mkdir(exist_ok=True)
    _handler = logging.FileHandler(LOG_FILE)
    _handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    _logger.addHandler(_handler)


def log_event(event, username="-", level="info"):
    # Remove line breaks so one event is always one line.
    safe_name = str(username).replace("\n", " ").replace("\r", " ")
    message = f'event={event} ip={request.remote_addr} username="{safe_name}"'
    getattr(_logger, level)(message)
