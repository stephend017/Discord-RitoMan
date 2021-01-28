from discord_ritoman.lol_match_metadata import LoLMatchMetadata
from unittest import mock

import discord_ritoman.lol_api
from discord_ritoman.lol_api import (
    get_account_id,
    get_matches,
    get_puuid,
    riot_api_get,
)
import pytest
import json


class MockResponse:
    def __init__(self, status_code, text="success", json_data={}):
        self.status_code = status_code
        self.text = text
        self.json_data = json_data

    def json(self):
        return self.json_data

    @property
    def ok(self):
        return self.status_code / 100 == 2


@mock.patch("discord_ritoman.lol_api.sys.exit")
@mock.patch.object(discord_ritoman.lol_api, "logger")
@mock.patch.object(discord_ritoman.lol_api.requests, "get")
def test_invalid_token(mock_get, mock_logger, mock_exit):
    """
    Tests that when an invalid token is sent in the request
    that the application logs the error and exits.
    """
    mock_get.return_value = MockResponse(403)

    def mock_exit_func(*args, **kwargs):
        raise SystemExit

    mock_exit.side_effect = mock_exit_func

    with pytest.raises(SystemExit):
        riot_api_get("thisisafakeurl")

    mock_logger.critical.assert_called_once()
    mock_exit.assert_called_once()


@mock.patch.object(discord_ritoman.lol_api, "logger")
@mock.patch.object(discord_ritoman.lol_api.requests, "get")
def test_api_rate_limit(mock_get, mock_logger):
    """
    Tests that when the a request returns as rate limited,
    the application logs the error, then queues the request
    to be run again in a set time (most likely 1 sec)
    """
    mock_get.return_value = MockResponse(429, "Rate Limit Exceeded")
    riot_api_get("thisisafakeurl")
    # TODO process defered request
    mock_logger.warn.assert_called_once()


@mock.patch.object(discord_ritoman.lol_api, "riot_api_get")
def test_get_account_id(mock_riot_api_get):
    """
    Tests that get account id returns the correct info
    """
    with open("./tests/mock/summoners_by-puuid.json") as fp:
        data = json.load(fp)
        mock_riot_api_get.return_value = data
        account_id = get_account_id("thisisapuuid")
        assert account_id == data["accountId"]


@mock.patch.object(discord_ritoman.lol_api, "riot_api_get")
def test_get_matches(mock_riot_api_get):
    """
    Tests that get matches returns the correct info
    """
    expected = [
        LoLMatchMetadata(3676639301, 24, 1606165409685),
        LoLMatchMetadata(3676685956, 86, 1606163888648),
    ]

    with open("./tests/mock/matchlists_by-account.json") as fp:
        data = json.load(fp)
        mock_riot_api_get.return_value = data
        matches = get_matches("thisisaaccountid", 1234)
        assert matches == expected


@mock.patch.object(discord_ritoman.lol_api, "riot_api_get")
def test_get_puuid(mock_riot_api_get):
    """
    Tests that get puuid returns thje correct info
    """
    with open("./tests/mock/summoners_by-name.json") as fp:
        data = json.load(fp)
        mock_riot_api_get.return_value = data
        account_id = get_puuid("thisisaname")
        assert account_id == data["puuid"]


@mock.patch.object(discord_ritoman.lol_api, "riot_api_get")
def test_cached_requests(mock_riot_api_get):
    """
    Tests that when the same request is made, the LRU correctly
    works and only executes the corresponding code once (returns cached result)
    """
    expected = "randomaccountid"
    mock_riot_api_get.return_value = {"accountId": "randomaccountid"}
    r0 = get_account_id("randompuuid")
    r1 = get_account_id("randompuuid")
    mock_riot_api_get.assert_called_once()
    assert expected == r0 == r1
