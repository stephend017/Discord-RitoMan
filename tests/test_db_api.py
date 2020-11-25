from discord_ritoman.utils import unix_time_millis
from discord_ritoman.db_api import (
    add_new_discord_user,
    add_new_lol_user,
    get_all_discord_users,
    get_all_prefixes,
    get_all_stat_prefixes_01,
    get_all_suffixes,
    get_cursor,
    get_last_recorded_time,
    set_last_recorded_time,
)
from unittest import mock
import discord_ritoman.db_api
import datetime


@mock.patch("os.getenv")
@mock.patch("psycopg2.connect")
def test_get_cursor(mock_connect, mock_getenv):
    """"""
    # return this when setting up db connection
    mock_getenv.return_value = "somedbpassword"

    # result of psycopg2.connect(**connection_stuff)
    mock_connect_cm = mock_connect.return_value
    # object assigned to con in with ... as connection
    mock_connection = mock_connect_cm.__enter__.return_value
    # object assigned to cursor in with ...  as cursor
    mock_cursor = mock_connection.cursor.return_value

    with get_cursor() as cursor:
        mock_connect.assert_called_once_with(
            dbname="root",
            user="root",
            password="somedbpassword",
            host="127.0.0.1",
            port=5432,
        )
        assert cursor is mock_cursor


@mock.patch.object(discord_ritoman.db_api, "get_cursor")
def test_get_all_discord_users(mock_get_cursor):
    """Tests that the method get all discord users works as expected"""
    expected = [["test_username_01", "test_riot_puuid_01", 1]]

    mock_cursor_cm = mock_get_cursor.return_value
    mock_cursor = mock_cursor_cm.__enter__.return_value
    mock_cursor.fetchall.return_value = expected
    actual = get_all_discord_users()

    mock_cursor.execute.assert_called_once_with("SELECT * FROM discord_users")
    mock_cursor.fetchall.assert_called_once()

    assert actual == expected


@mock.patch.object(discord_ritoman.db_api, "get_cursor")
def test_get_last_recorded_time(mock_get_cursor):
    """Tests that the method get last recorded time works as expected"""
    expected = 1000

    mock_cursor_cm = mock_get_cursor.return_value
    mock_cursor = mock_cursor_cm.__enter__.return_value
    mock_cursor.fetchall.return_value = [[expected]]
    actual = get_last_recorded_time("username")

    mock_cursor.execute.assert_called_once_with(
        "SELECT last_game_recorded FROM lol_data WHERE discord_username=%(discord_username)s",
        {"discord_username": "username"},
    )
    mock_cursor.fetchall.assert_called_once()

    assert actual == expected


@mock.patch.object(discord_ritoman.db_api, "get_cursor")
def test_set_last_recorded_time(mock_get_cursor):
    """Tests that the method set last recorded time works as expected"""

    mock_cursor_cm = mock_get_cursor.return_value
    mock_cursor = mock_cursor_cm.__enter__.return_value
    set_last_recorded_time("username", 1000)

    mock_cursor.execute.assert_called_once_with(
        "UPDATE lol_data SET last_game_recorded = %(last_game_recorded)s WHERE discord_username=%(discord_username)s",
        {"discord_username": "username", "last_game_recorded": 1000},
    )


@mock.patch.object(discord_ritoman.db_api, "get_cursor")
def test_get_all_prefixes(mock_get_cursor):
    """Tests that the method get all prefixes works as expected"""
    expected = [["text_01"], ["text_02"]]

    mock_cursor_cm = mock_get_cursor.return_value
    mock_cursor = mock_cursor_cm.__enter__.return_value
    mock_cursor.fetchall.return_value = expected
    actual = get_all_prefixes()

    mock_cursor.execute.assert_called_once_with("SELECT * FROM prefixes")
    mock_cursor.fetchall.assert_called_once()

    assert actual == expected


@mock.patch.object(discord_ritoman.db_api, "get_cursor")
def test_get_all_stat_prefixes_01(mock_get_cursor):
    """Tests that the method get all stat prefixes 01 works as expected"""
    expected = [["text_01"], ["text_02"]]

    mock_cursor_cm = mock_get_cursor.return_value
    mock_cursor = mock_cursor_cm.__enter__.return_value
    mock_cursor.fetchall.return_value = expected
    actual = get_all_stat_prefixes_01()

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM stat_prefixes_01"
    )
    mock_cursor.fetchall.assert_called_once()

    assert actual == expected


@mock.patch.object(discord_ritoman.db_api, "get_cursor")
def test_get_all_suffixes(mock_get_cursor):
    """Tests that the method get all suffixes works as expected"""
    expected = [["text_01"], ["text_02"]]

    mock_cursor_cm = mock_get_cursor.return_value
    mock_cursor = mock_cursor_cm.__enter__.return_value
    mock_cursor.fetchall.return_value = expected
    actual = get_all_suffixes()

    mock_cursor.execute.assert_called_once_with("SELECT * FROM suffixes")
    mock_cursor.fetchall.assert_called_once()

    assert actual == expected


@mock.patch.object(discord_ritoman.db_api, "get_cursor")
def test_add_discord_user_succeeded(mock_get_cursor):
    """
    Tests that when adding a new discord user succeeds,
    it returns True
    """
    mock_cursor_cm = mock_get_cursor.return_value
    mock_cursor = mock_cursor_cm.__enter__.return_value

    discord_username: str = "test_username"
    riot_puuid: str = "test_puuid"
    discord_id: int = 0

    result = add_new_discord_user(discord_username, riot_puuid, discord_id)
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO discord_users (discord_username, riot_puuid, discord_id) VALUES (%(discord_username)s, %(riot_puuid)s, %(discord_id)s)",
        {
            "discord_username": discord_username,
            "riot_puuid": riot_puuid,
            "discord_id": discord_id,
        },
    )

    assert result is True


@mock.patch.object(discord_ritoman.db_api, "logger")
@mock.patch.object(discord_ritoman.db_api, "get_cursor")
def test_add_discord_user_failed(mock_get_cursor, mock_logger):
    """
    Tests that when adding a new discord user fails, it properly
    logs the error, and returns False
    """
    mock_cursor_cm = mock_get_cursor.return_value
    mock_cursor = mock_cursor_cm.__enter__.return_value

    def mock_error(*args, **kwargs):
        raise Exception("test error")

    mock_cursor.execute.side_effect = mock_error

    result = add_new_discord_user("test_username", "test_puuid", 0)

    mock_logger.critical.assert_called_once_with("ERROR: test error")
    assert result is False


@mock.patch("discord_ritoman.db_api.datetime")
@mock.patch.object(discord_ritoman.db_api, "get_cursor")
def test_add_lol_data_succeeded(mock_get_cursor, mock_datetime):
    """
    Tests that when adding new lol data succeeds,
    it returns True
    """
    mock_cursor_cm = mock_get_cursor.return_value
    mock_cursor = mock_cursor_cm.__enter__.return_value

    discord_username: str = "test_username"

    mock_datetime.now.return_value = datetime.datetime(2020, 1, 1, 12, 1, 1)
    mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(
        *args, **kw
    )
    timestamp = datetime.datetime(2020, 1, 1, 12, 1, 1)

    result = add_new_lol_user(discord_username)
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO lol_data (discord_username, last_game_recorded) VALUES (%(discord_username)s, %(last_game_recorded)s)",
        {
            "discord_username": discord_username,
            "last_game_recorded": int(unix_time_millis(timestamp)),
        },
    )

    assert result is True


@mock.patch.object(discord_ritoman.db_api, "logger")
@mock.patch.object(discord_ritoman.db_api, "get_cursor")
def test_add_lol_data_failed(mock_get_cursor, mock_logger):
    """
    Tests that when adding new lol data fails, it properly
    logs the error, and returns False
    """
    mock_cursor_cm = mock_get_cursor.return_value
    mock_cursor = mock_cursor_cm.__enter__.return_value

    def mock_error(*args, **kwargs):
        raise Exception("test error")

    mock_cursor.execute.side_effect = mock_error

    result = add_new_lol_user("test_username")

    mock_logger.critical.assert_called_once_with("ERROR: test error")
    assert result is False
