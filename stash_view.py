import stash
from clear import clear


def files_created(with_error):
    clear()

    if with_error:
        print("Invalid...")
    else:
        print("Created required files...")

    print("Run python stash.py <keyword> <password>")


def after_search_option(account_id):
    error = None

    while True:
        if error is not None:
            print(error)

        print("\n[e]dit -- [d]elete -- [q]uit\n")
        option = input(">> ")
        if option not in list("edq"):
            error = "Invalid input"
        else:
            break

    stash.after_search_action(account_id, option)


def show_result_from_keyword(details, keyword, error=None):
    clear()
    if error is not None:
        print(error)
    if not details:
        print(f"{keyword} not found\n")
    else:
        account_id, username, password = details
        print(f"{keyword}")
        print(f"username: {username}\npassword: {password}")
        after_search_option(account_id)


def show_all_results(accounts):
    if not accounts:
        print("Database is empty")
    else:
        print("Keyword  | Username | Password")
        for account in accounts:
            keyword, username, password = account
            print(f"{keyword} | {username} | {password}")


def get_password_options():
    questions = [
        "Include uppercase? (y/n): ",
        "include digits? (y/n): ",
        "include special characters? (y/n): ",
    ]
    selected = [
        "y",
    ]
    response = ""

    for question in questions:
        while response not in list("yn"):
            response = input(question)
        selected.append(response)
        response = ""

    while True:
        try:
            char_len = int(input("Character length?: "))
        except ValueError:
            print("Invalid input...")
        else:
            break
    generated_password = stash.generate_password(selected, char_len)

    return generated_password


def get_account_details():
    not_allowed = ["/", "\\", "''", '""']
    account_details = []
    required_details = ["Keyword", "Username", "Password"]
    option = ""

    while option not in list("yn"):
        option = input("Generate password? (y/n): ")

    if option == "y":
        generated_password = get_password_options()
        required_details.pop()

    for required_detail in required_details:
        clear()
        is_allowed = True
        while is_allowed:
            print(f"Not allowed characters {not_allowed}")
            detail = input(f"Enter {required_detail}: ")
            is_allowed = any(item in list(detail) for item in not_allowed)
            if is_allowed:
                print("Invalid character found...\n")

        account_details.append(detail)

    if len(account_details) < 3:
        account_details.append(generated_password)

    return account_details


def choose_to_edit():
    option = ""
    error = None

    while True:
        if error is not None:
            print(error)

        print("Choose what to edit...")
        option = input("[u]sername - [p]assword - [k]eyword: ")
