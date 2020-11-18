from discord_ritoman.db_api import (
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
