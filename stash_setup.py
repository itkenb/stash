import os
from getpass import getpass

import stash_database as sd
import stash_encryption as se


def check_required_files():
    is_valid = True

    if not os.path.exists("stash_encryption.key"):
        se.create_encryption_key()
        print("Encryption key created...")
        is_valid = False
    else:
        print("Encryption key found...")

    if not os.path.exists("stash_user.key"):
        user_password = getpass("Setup a password for stash: ")
        se.create_user_key(user_password)
        print("User key created...")
        is_valid = False
    else:
        print("User key found...")

    if not os.path.exists("stash.db"):
        sd.create_database()
        print("Database created...")
        is_valid = False
    else:
        print("Database found...")

    # if not os.path('creads.json'):
    # print("Google sheet credentials not found...")
    # else:
    # print("Google sheet credentials found...")

    return is_valid
