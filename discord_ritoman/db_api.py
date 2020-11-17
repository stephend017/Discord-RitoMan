"""
Interface for using the database


source for restarting db on linux
https://stackoverflow.com/questions/46936368/could-not-connect-to-server-postgresql-connecting-to-unix-domain-socket/46936946

source for setting up db on linux
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04#step-3-%E2%80%94-creating-a-new-role
"""

import psycopg2
from psycopg2.extras import DictCursor
from contextlib import contextmanager
import os

@contextmanager
def get_cursor():
    """
    """
    with psycopg2.connect(
        dbname="stephen",
        user="stephen",
        password=os.getenv("DB_PASS", ""),
        host="127.0.0.1",
        port=5432,
    ) as connection:
        yield connection.cursor(cursor_factory=DictCursor)
        connection.commit()


def get_all_discord_users():
    """
    """
    data = {}
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM discord_users")
        data = cursor.fetchall()
    return data


def get_last_recorded_time(discord_username: str) -> int:
    """
    """
    data = {}
    with get_cursor() as cursor:
        cursor.execute(
            "SELECT last_game_recorded FROM lol_data WHERE discord_username=%(discord_username)s",
            {"discord_username": discord_username},
        )
        data = cursor.fetchall()
    return data[0][0]


def set_last_recorded_time(discord_username: str, timestamp: int):
    """
    """
    with get_cursor() as cursor:
        cursor.execute(
            "UPDATE lol_data SET last_game_recorded = %(last_game_recorded)s WHERE discord_username=%(discord_username)s",
            {
                "discord_username": discord_username,
                "last_game_recorded": timestamp,
            },
        )


def get_all_prefixes():
    """
    """
    data = {}
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM prefixes",)
        data = cursor.fetchall()
    return data


def get_all_stat_prefixes_01():
    """
    """
    data = {}
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM stat_prefixes_01",)
        data = cursor.fetchall()
    return data


def get_all_suffixes():
    """
    """
    data = {}
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM suffixes",)
        data = cursor.fetchall()
    return data
