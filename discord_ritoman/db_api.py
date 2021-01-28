"""
Interface for using the database


source for restarting db on linux
https://stackoverflow.com/questions/46936368/could-not-connect-to-server-postgresql-connecting-to-unix-domain-socket/46936946

source for setting up db on linux
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04#step-3-%E2%80%94-creating-a-new-role
"""

from datetime import datetime
from discord_ritoman.models import GameResult
from typing import Any, Callable, List, Tuple
import psycopg2
from psycopg2.extras import DictCursor
from contextlib import contextmanager
import os
from discord_ritoman.utils import unix_time_millis
import functools
import logging
from logging.handlers import RotatingFileHandler

log_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s"
)

logFile = "./db.log"

my_handler = RotatingFileHandler(
    logFile,
    mode="a",
    maxBytes=5 * 1024 * 1024,
    backupCount=2,
    encoding=None,
    delay=0,
)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

logger = logging.getLogger("db")
logger.setLevel(logging.INFO)

logger.addHandler(my_handler)


@contextmanager
def get_cursor():
    """
    Connects to the Database using credentials stored
    in environment variables

    Returns:
        contextmanager: A context manager of the cursor object
    """
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


def db_insert(func: Callable):
    """
    Wrapper for database insert functions.

    This wrapper provides logging and basic error
    handling for db functions

    Args:
        func (Callable): the database insert function to call

    Returns:
        Callable: function that calls the passed in function
            and logs errors
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as error:
            logger.critical(f"ERROR: {error}")
            return False
        return True

    return wrapper


def db_delete(func: Callable):
    """
    Wrapper for database delete functions.

    This wrapper provides logging and basic error
    handling for db functions

    Args:
        func (Callable): the database delete function to call

    Returns:
        Callable: function that calls the passed in function
            and logs errors
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as error:
            logger.critical(f"ERROR: {error}")
            return False
        return True

    return wrapper


def db_update(func: Callable):
    """
    Wrapper for database update functions.

    This wrapper provides logging and basic error
    handling for db functions

    Args:
        func (Callable): the database update function to call

    Returns:
        Callable: function that calls the passed in function
            and logs errors
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as error:
            logger.critical(f"ERROR: {error}")
            return False
        return True

    return wrapper


def db_select(func: Callable):
    """
    Wrapper for database select functions.

    This wrapper provides logging and basic error
    handling for db functions

    Args:
        func (Callable): the database select function to call

    Returns:
        Callable: function that calls the passed in function
            and logs errors
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            return data
        except Exception as error:
            logger.critical(f"ERROR: {error}")
            return None

    return wrapper


@db_select
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


@db_select
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
    data: int = 0
    with get_cursor() as cursor:
        cursor.execute(
            "SELECT last_game_recorded FROM lol_data WHERE discord_username=%(discord_username)s",
            {"discord_username": discord_username},
        )
        data = cursor.fetchall()
    return data[0][0]


@db_update
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


@db_select
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


@db_select
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


@db_select
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


@db_insert
def add_new_discord_user(
    discord_username: str, riot_puuid: str, discord_id: int
) -> bool:
    """
    Adds a new discord user to the DB

    Note: Errored operations will log the error to the db logfile

    Args:
        discord_username (str): the username of the discord member
        riot_puuid       (str): the riot_puuid of the discord member
        discord_id       (int): the numeric discord id of the
                                discord member

    Returns:
        bool: True if succeeded, False otherwise
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


@db_insert
def opt_in_record_lol_winrate(discord_username: str) -> bool:
    """
    Adds a user to the winrate db  for LoL games

    Args:
        discord_username (str): the username of the discord member

    Returns:
        bool: True if the operation succeeded, False otherwise
    """
    with get_cursor() as cursor:
        cursor.execute(
            "INSERT INTO lol_winrate (discord_username, win_count, loss_count) VALUES (%(discord_username)s, %(win_count)s, %(loss_count)s)",
            {
                "discord_username": discord_username,
                "win_count": 0,
                "loss_count": 0,
            },
        )


@db_delete
def opt_out_record_lol_winrate(discord_username: str) -> bool:
    """
    Adds a user to the winrate db  for LoL games

    Args:
        discord_username (str): the username of the discord member

    Returns:
        bool: True if the operation succeeded, False otherwise
    """
    with get_cursor() as cursor:
        cursor.execute(
            "DELETE FROM lol_winrate WHERE discord_username = %(discord_username)s",
            {"discord_username": discord_username},
        )


@db_insert
def add_new_lol_user(discord_username: str) -> bool:
    """
    Adds a new user to be tracked for LoL games

    Note: Errored operations will log the error to the db logfile

    Args:
        discord_username (str): the username of the discord member

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    timestamp = int(unix_time_millis(datetime.now()))
    with get_cursor() as cursor:
        cursor.execute(
            "INSERT INTO lol_data (discord_username, last_game_recorded) VALUES (%(discord_username)s, %(last_game_recorded)s)",
            {
                "discord_username": discord_username,
                "last_game_recorded": timestamp,
            },
        )


@db_select
def get_discord_lol_record(discord_username: str) -> List[int]:
    """
    Returns a tuple of the given users, win / loss record for league games
    that day

    Args:
        discord_username (str): the username of the discord member

    Returns:
        List[int]: the game record for the given discord user.
    """
    data = {}
    with get_cursor() as cursor:
        cursor.execute(
            "SELECT win_count, loss_count FROM lol_winrate WHERE discord_username = %(discord_username)s",
            {"discord_username": discord_username},
        )
        data = cursor.fetchall()
    return data[0]


@db_select
def get_all_lol_users_winrate() -> List[List[Any]]:
    """
    returns the winrate for all users in the winrate db

    Returns:
        List[List[Any]]: a list of users in the winrate db
    """
    result = []
    with get_cursor() as cursor:
        cursor.execute(
            "SELECT discord_id, win_count, loss_count FROM lol_winrate INNER JOIN discord_users on lol_winrate.discord_username = disocrd_users.discord_username"
        )
        result = cursor.fetchall()
    return result


@db_update
def add_new_lol_game(discord_username: str, game_result: GameResult) -> bool:
    """
    Adds a new game result to the db

    Note this db is wiped after dumped

    Args:
        discord_username (str): the username of the discord member
        game_result (GameResult): the result of the game

    Returns:
        bool: True if the operation was successful, False otherwise
    """
    record = get_discord_lol_record(discord_username)
    with get_cursor() as cursor:
        cursor.execute(
            "UPDATE lol_winrate SET win_count = %(win_count)s, loss_count = %(loss_count)s WHERE discord_username = %(discord_username)s",
            {
                "win_count": (1 if game_result == GameResult.WIN else 0)
                + record[0],
                "loss_count": (1 if game_result == GameResult.LOSS else 0)
                + record[1],
                "discord_username": discord_username,
            },
        )


@db_update
def reset_all_lol_user_winrates() -> bool:
    """
    Resets the winrate of all users back to 0-0

    Returns:
        bool: True if the operation succeeds, false otherwise
    """
    with get_cursor() as cursor:
        cursor.execute(
            "UPDATE lol_winrate SET win_count = %(win_count)s, loss_count = %(loss_count)s",
            {"win_count": 0, "loss_count": 0},
        )


@db_select
def does_user_record_lol_winrate(discord_username: str) -> bool:
    """
    Returns true if the user records winrate, false otherwise

    Args:
        discord_username (str): the username of ther discord member

    Returns:
        bool: True if the user exists, False otherwise
    """
    result = 0
    with get_cursor() as cursor:
        cursor.execute(
            "SELECT count(*) FROM lol_winrate WHERE discord_username = %(discord_username)s",
            {"discord_username": discord_username},
        )
        result = cursor.fetchall()[0]
    return result > 0
