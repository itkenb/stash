import os
from getpass import getpass

from cryptography.fernet import Fernet


def get_encryption_key():
    with open("stash_encryption.key", "rb") as file:
        key = file.read()

    return key


def create_encryption_key():
    key = Fernet.generate_key()

    with open("stash_encryption.key", "wb") as file:
        file.write(key)


def create_user_key(user_password):
    key = get_encryption_key()
    fe = Fernet(key)
    user_key = fe.encrypt(user_password.encode())

    with open("stash_user.key", "wb") as file:
        file.write(user_key)


def decrypt_user_key():
    key = get_encryption_key()

    with open("stash_user.key", "rb") as file:
        e_user_key = file.read()

    fe = Fernet(key)
    user_key = fe.decrypt(e_user_key).decode()

    return user_key


def decrypt_password(e_password):
    key = get_encryption_key()
    fe = Fernet(key)
    password = fe.decrypt(e_password).decode()

    return password
