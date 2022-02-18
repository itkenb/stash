import random
import string
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


def search_keyword(keyword):

    details = sd.get_account_details(keyword)
    if details is None:
        return False
    else:
        return details


def get_all():
    accounts = sd.get_all_accounts()
    if accounts is None:
        return False
    else:
        return accounts


def generate_password(response, min_len, max_len):
    password_characters = ""
    lower_letters = string.ascii_lowercase
    upper_letters = string.ascii_uppercase
    numbers = string.digits
    punctuations = "~!@#$%^&*()_-+={}[]|:;,<>.?"
    options = [lower_letters, upper_letters, numbers, punctuations]
    random_len = random.randint(min_len, max_len)

    for res in enumerate(response):
        if res[1] == "y":
            password_characters = password_characters + options[res[0]]
    generated_password = "".join(
        (random.choice(password_characters) for i in range(random_len))
    )
    print(generate_password)


def controller(keyword, user_password):
    is_allowed = check_authentication(user_password)
    if is_allowed:
        if keyword == "-a":
            print("add")
        elif keyword == "-e":
            print("export")
        elif keyword == "-g":
            options = "yn"
            response = "y"
            res = "x"
            valid_input = False
            min_len = 8
            max_len = 16
            while res not in options:
                res = input("include uppercase? y/n: ")
            response = response + res
            res = "x"
            while res not in options:
                res = input("include numbers? y/n: ")
            response = response + res
            res = "x"
            while res not in options:
                res = input("include special characters? y/n: ")
            response = response + res
            while not valid_input:
                try:
                    min_len = int(input("Min length?: "))
                except ValueError as error:
                    print("Invalid input")
                else:
                    valid_input = True
            valid_input = False
            while not valid_input:
                try:
                    min_len = int(input("Max length?: "))
                except ValueError as error:
                    print("Invalid input")
                else:
                    valid_input = True
            generate_password(response, min_len, max_len)
        elif keyword == "-i":
            print("import")
        elif keyword == "-sa":
            accounts = get_all()
            if not accounts:
                print("Database is empty")
            else:
                print("Keyword  | Username  | Password")
                for account in accounts:
                    keyword, username, e_password = account
                    password = se.decrypt_password(e_password)
                    print(f"{keyword} | {username} | {password}")
        else:
            details = search_keyword(keyword)
            if not details:
                print(f"{keyword} not found")
            else:
                account_id, username, e_password = details
                password = se.decrypt_password(e_password)
                print(f"{keyword}")
                print(f"username: {username}\npassword: {password}")
                print("\ncopy [u]sername || copy [p]assword")
                print("[e]dit || [d]elete\n")
                print(account_id)
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
