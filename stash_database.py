import sqlite3
from sqlite3 import Error


def create_database():
    query = "create table if not exists accounts\
            (account_id INTEGER PRIMARY KEY,\
            keyword TEXT,\
            username TEXT,\
            password TEXT,\
            sync_status INTEGER)"

    conn = None

    try:
        conn = sqlite3.connect("stash.db")
    except Error as e:
        print(e)
    finally:
        c = conn.cursor()
        c.execute(query)

    conn.close()
