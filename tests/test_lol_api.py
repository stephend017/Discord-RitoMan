from unittest import mock
import discord_ritoman.lol_api


# @mock.patch("discord_ritoman.lol_api.sys.exit")
@mock.patch.object(discord_ritoman.lol_api.requests, "get")
def test_invalid_token(mock_get):
    """
    Tests that when an invalid token is sent in the request
    that the application logs the error and exits.
    """
    # TODO
    pass


@mock.patch.object(discord_ritoman.lol_api.requests, "get")
def test_api_rate_limit(mock_get):
    """
    Tests that when the a request returns as rate limited,
    the application logs the error, then queues the request
    to be run again in a set time (most likely 1 sec)
    """
    # TODO
    pass


@mock.patch.object(discord_ritoman.lol_api, "riot_api_get")
def test_get_account_id(mock_riot_api_get):
    """
    Tests that get account id returns the correct info
    """
    # TODO
    pass


@mock.patch.object(discord_ritoman.lol_api, "riot_api_get")
def test_get_matches(mock_riot_api_get):
    """
    Tests that get matches returns the correct info
    """
    # TODO
    pass


@mock.patch.object(discord_ritoman.lol_api, "riot_api_get")
def test_get_puuid(mock_riot_api_get):
    """
    Tests that get puuid returns thje correct info
    """
    # TODO
    pass
