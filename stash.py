import random
import string
import sys

import stash_database as sd
import stash_encryption as se
import stash_setup as ss
import stash_view as sv
from clear import clear


def check_authentication(user_password):
    is_allowed = False
    user_key = se.decrypt_user_key()

    if user_key == user_password:
        is_allowed = True

    return is_allowed


def generate_password(selected, char_len):
    password_characters = ""
    lower_letters = string.ascii_lowercase
    upper_letters = string.ascii_uppercase
    numbers = string.digits
    punctuations = "~!@#$%^&*()_-+={}[]|:;,<>.?"
    options = [lower_letters, upper_letters, numbers, punctuations]

    for res in enumerate(selected):
        if res[1] == "y":
            password_characters = password_characters + options[res[0]]

    generated_password = "".join(
        (random.choice(password_characters) for i in range(char_len))
    )
    return generated_password


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


def add_account(account_details):
    keyword = account_details[0]
    details = search_keyword(keyword)
    if not details:
        password = se.encrypt_password(account_details[2])
        account_details[2] = password
        is_inserted = sd.insert_account(account_details)
        if is_inserted is not None:
            details = search_keyword(keyword)
            password = se.decrypt_password(details[2])
            details = list(details)
            details[2] = password
            sv.show_result_from_keyword(details, keyword, error="Account added...")
    else:
        password = se.decrypt_password(details[2])
        details = list(details)
        details[2] = password
        sv.show_result_from_keyword(details, keyword, error="Account already exist...")


def edit_account(account_id):
    option = sv.choose_to_edit()
    pass


def after_search_action(account_id, option):
    if option == "e":
        keyword = edit_account(account_id)
    elif option == "d":
        pass
    elif option == "q":
        quit()


def controller(keyword, user_password):
    is_allowed = check_authentication(user_password)
    if is_allowed:
        if keyword == "-a":
            account_details = sv.get_account_details()
            add_account(account_details)
        elif keyword == "-e":
            print("export")
        elif keyword == "-i":
            print("import")
        elif keyword == "-sa":
            accounts = get_all()
            if not accounts:
                sv.show_all_results(accounts)
            else:
                for account in enumerate(accounts):
                    password = se.decrypt_password(account[1][2])
                    account_details = list(account[1])
                    account_details[2] = password
                    accounts[account[0]] = account_details

                sv.show_all_results(accounts)
        else:
            details = search_keyword(keyword)
            if not details:
                sv.show_result_from_keyword(details, keyword)
            else:
                password = se.decrypt_password(details[2])
                details = list(details)
                details[2] = password
                sv.show_result_from_keyword(details, keyword)
    else:
        print("Invalid password...")


def check_args(is_valid):
    if len(sys.argv) == 3:
        if is_valid:
            clear()
            controller(sys.argv[1], sys.argv[2])
        else:
            sv.files_created(with_error=False)
    else:
        if is_valid:
            sv.files_created(with_error=True)
        else:
            sv.files_created(with_error=False)


if __name__ == "__main__":
    is_valid = ss.check_required_files()
    check_args(is_valid)
