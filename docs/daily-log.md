# Daily Log

## 12 Oct
- Created the repo and wrote the full project plan in the README
- Next: set up Codespaces and run a Flask "Hello World"

## 13 Oct
- Added .gitignore, requirements.txt, app.py and templates/index.html
- Set up Codespaces and ran the Flask app
- Confirmed Hello World with curl (browser port forwarding failed on my tablet)
- Learned: how to use a Codespace and test a web app from the terminal
- ![Flask Hello World running in Codespaces](Screenshot_20261013_184005_Chrome.jpg)

## 14 Oct
- Built registration, login, dashboard and logout with SQLite (insecure on purpose)
- Wrote docs/insecure-design-notes.md listing the weaknesses to attack and fix
- Learned: how Flask routes, forms and sessions fit together
- Next: add logging to a log file

## Thu 15 Oct
- Added logging to the app on the school PC: app_logging.py and log_event calls in every route
- Did not push the commits, so they never reached GitHub
- Decided not to go back to that PC and to redo the work instead
- Learned: commit and push before leaving a machine
- Next: rebuild logging on 16 Oct

## Fri 16 Oct
- Rebuilt the logging, since the 15 Oct work was never pushed
- Codespaces would not load, so I edited on GitHub and tested on the school PC
- Logs go to logs/app.log: registration, login, database errors, dashboard access and logout
- Tested with curl: register_success, login_success, login_failed and dashboard_denied all logged (screenshot in docs/)
- Documented the log format in docs/log-format.md
- Next: Attack 1, SQL injection on the login form