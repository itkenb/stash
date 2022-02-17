import os
import sqlite3
from getpass import getpass
from sqlite3 import Error

from cryptography.fernet import Fernet


def create_encryption_key():
    key = Fernet.generate_key()

    with open("stash_encryption.key", "wb") as file:
        file.write(key)


def create_user_key():
    user_password = getpass("Setup a password for stash: ")

    with open("stash_encryption.key", "rb") as file:
        key = file.read()

    encoded_password = user_password.encode()
    fe = Fernet(key)
    user_key = fe.encrypt(encoded_password)

    with open("stash_user.key", "wb") as file:
        file.write(user_key)


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


def check_required_files():
    if not os.path.exists("stash_encryption.key"):
        create_encryption_key()
        print("Encryption key created...")
    else:
        print("Encryption key found...")

    if not os.path.exists("stash_user.key"):
        create_user_key()
        print("User key created...")
    else:
        print("User key found...")

    if not os.path.exists("stash.db"):
        create_database()
        print("Database created...")
    else:
        print("Database found...")

    # if not os.path('creads.json'):
    # print("Google sheet credentials not found...")
    # else:
    # print("Google sheet credentials found...")
