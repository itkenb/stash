import sqlite3
from sqlite3 import Error

import stash_encryption as se


def create_database():
    with sqlite3.connect("stash.db") as conn:
        cursor = conn.cursor()
        query = """create table if not exists accounts\
                (account_id INTEGER PRIMARY KEY,\
                keyword TEXT,\
                username TEXT,\
                password TEXT,\
                sync_status INTEGER)"""
        cursor.execute(query)


def get_account_details(keyword):
    with sqlite3.connect("stash.db") as conn:
        cursor = conn.cursor()
        query = """select account_id, username, password\
                from accounts\
                where keyword = ?"""
        cursor.execute(query, (keyword,))
        details = cursor.fetchone()

        return details


def get_all_accounts():
    with sqlite3.connect("stash.db") as conn:
        query = """select keyword, username, password from accounts"""
        cursor = conn.cursor()
        cursor.execute(query)
        accounts = cursor.fetchall()

        return accounts


def insert_account(account_details):
    keyword, username, password = account_details

    with sqlite3.connect("stash.db") as conn:
        query = """insert into accounts\
                (keyword, username, password, sync_status)\
                values(?, ?, ?, ?)"""
        cursor = conn.cursor()
        is_inserted = cursor.execute(
            query,
            (
                keyword,
                username,
                password,
                1,
            ),
        )

    return is_inserted
