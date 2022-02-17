import sys

import stash_database as sd
import stash_encryption as se
import stash_setup as ss
from clear import clear


def check_authentication(user_password):
    is_allowed = False
    user_key = se.decrypt_user_key()

    if user_key == user_password:
        is_allowed = True

    return is_allowed


def controller(keyword, user_password):
    is_allowed = check_authentication(user_password)
    if is_allowed:
        if keyword == "-a":
            print("add")
        elif keyword == "-d":
            print("delete")
        elif keyword == "-e":
            print("edit")
        elif keyword == "-g":
            print("generate")
        else:
            print(f"search {keyword}")
    else:
        print("Invalid password...")


def check_args(is_valid):
    if len(sys.argv) == 3:
        if is_valid:
            clear()
            controller(sys.argv[1], sys.argv[2])
        else:
            clear()
            print(
                "Created required files...\
                    \nRun python stash.py <keyword> <password>"
            )
    else:
        if is_valid:
            clear()
            print("Invalid... \nRun python stash.py <keyword> <password>")
        else:
            clear()
            print(
                "Created required files...\
                    \nRun python stash.py <keyword> <password>"
            )


if __name__ == "__main__":
    is_valid = ss.check_required_files()
    check_args(is_valid)
