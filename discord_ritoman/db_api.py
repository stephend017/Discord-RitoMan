"""
Interface for using the database


source for restarting db on linux
https://stackoverflow.com/questions/46936368/could-not-connect-to-server-postgresql-connecting-to-unix-domain-socket/46936946

source for setting up db on linux
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04#step-3-%E2%80%94-creating-a-new-role
"""

from datetime import datetime
from typing import Any, List
import psycopg2
from psycopg2.extras import DictCursor
from contextlib import contextmanager
import os
from discord_ritoman.utils import unix_time_millis


@contextmanager
def get_cursor():
    """"""
    db_pass = os.getenv("DB_PASS", None)
    if db_pass is None:
        raise Exception("Failed to load password from enviroment")

    with psycopg2.connect(
        dbname="root",
        user="root",
        password=db_pass,
        host="127.0.0.1",
        port=5432,
    ) as connection:
        yield connection.cursor(cursor_factory=DictCursor)
        connection.commit()


def get_all_discord_users() -> List[List[Any]]:
    """
    Returns a list of all discord users with thier riot PUUID and discord id

    Returns:
        List[List[Any]]: The list of discord users where each sub list is a
            discord users information. Each sublist has the following format
            - discord_username (str): this is the screen name for each user
            - riot_puuid (str): this is the puuid assigned to this user by
                riot games API
            - discord_id (int): this is the numeric ID representing this
                discord user in the discord server
    """
    data = []
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM discord_users")
        data = cursor.fetchall()
    return data


def get_last_recorded_time(discord_username: str) -> int:
    """
    Returns ms passed since epoch of the last recorded game
    for a given discord user

    Args:
        discord_username (str): the username of the discord member

    Returns:
        int: ms passed since the epoch of the last recorded game
            for this user
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
    Updates the last recorded game time for a given user

    Args:
        discord_username (str): the username of the discord member
        timestamp (int): the new last recorded game time in ms
            since epoch
    """
    with get_cursor() as cursor:
        cursor.execute(
            "UPDATE lol_data SET last_game_recorded = %(last_game_recorded)s WHERE discord_username=%(discord_username)s",
            {
                "discord_username": discord_username,
                "last_game_recorded": timestamp,
            },
        )


def get_all_prefixes() -> List[List[str]]:
    """
    Returns all prefixes for game loss message.

    This is the text that appears before the username in
    the message that is sent to the discord

    Returns:
        List[List[str]]: a list of lists where each sublist
            contains 1 element which is the prefix
    """
    data = {}
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM prefixes")
        data = cursor.fetchall()
    return data


def get_all_stat_prefixes_01() -> List[List[str]]:
    """
    Returns all stat prefixes for game loss message.

    This is the text that appears after the username in
    the message that is sent to the discord

    Returns:
        List[List[str]]: a list of lists where each sublist
            contains 1 element which is the stat prefix
    """
    data = {}
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM stat_prefixes_01")
        data = cursor.fetchall()
    return data


def get_all_suffixes() -> List[List[str]]:
    """
    Returns all suffixes for game loss message.

    This is the text that appears at the end of
    the message that is sent to the discord

    Returns:
        List[List[str]]: a list of lists where each sublist
            contains 1 element which is the suffix
    """
    data = {}
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM suffixes")
        data = cursor.fetchall()
    return data


def add_new_discord_user(discord_username, riot_puuid, discord_id):
    """
    Adds a new discord user to the DB
    """

    with get_cursor() as cursor:
        cursor.execute(
            "INSERT INTO discord_users (discord_username, riot_puuid, discord_id) VALUES (%(discord_username)s, %(riot_puuid)s, %(discord_id)s)",
            {
                "discord_username": discord_username,
                "riot_puuid": riot_puuid,
                "discord_id": discord_id,
            },
        )


def add_new_lol_user(discord_username):
    """
    Adds a new user to be tracked for LoL games
    """
    timestamp = int(unix_time_millis(datetime.datetime.now()))
    with get_cursor() as cursor:
        cursor.execute(
            "INSERT INTO lol_data (discord_username, last_game_recorded) VALUES (%(discord_username)s, %(last_game_recorded)s)",
            {
                "discord_username": discord_username,
                "last_game_recorded": timestamp,
            },
        )
