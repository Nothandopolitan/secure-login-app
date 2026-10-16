# Log Format

File: logs/app.log

Each line: date time LEVEL event=<name> ip=<address> username="<name>"

| Event | Level | Meaning |
|---|---|---|
| register_success | INFO | New account created |
| register_failed | WARNING | Registration failed (username taken or bad input) |
| login_success | INFO | Correct username and password |
| login_failed | WARNING | Wrong username or password |
| database_error | ERROR | A database query failed (often a sign of SQL injection) |
| dashboard_denied | WARNING | Dashboard requested without logging in |
| logout | INFO | User logged out |