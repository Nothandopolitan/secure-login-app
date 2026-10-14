import sqlite3

DATABASE = "users.db"


def get_db():
    return sqlite3.connect(DATABASE)


def init_db():
    db = get_db()
    db.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "username TEXT NOT NULL UNIQUE, "
        "password TEXT NOT NULL)"
    )
    db.commit()
    db.close()
