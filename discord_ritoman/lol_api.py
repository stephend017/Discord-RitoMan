"""
Interface for accessing riot API
"""
from typing import Any
from discord_ritoman.lol_match_metadata import LoLMatchMetadata
import requests
import os
import logging

logger = logging.Logger("LoL API Logger")
logger.addHandler(logging.FileHandler("./lol_api.log"))

RIOT_TOKEN = os.getenv("RIOT_TOKEN", None)


def riot_api_get(url: str) -> Any:
    """
    Generic method for making a GET request to the riot API

    Args:
        url (str): the url endpoint of the request

    Returns:
        Any: the json object returned by a successful request
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": RIOT_TOKEN,
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()

    logger.critical(
        f"GET riot request failed: URL: [{url}] [{response.status_code}] {response.text}"
    )
    raise Exception(
        f"GET riot request failed: URL: [{url}] [{response.status_code}] {response.text}"
    )


def get_account_id(puuid: str) -> str:
    """
    Returns the accountId for a given riot puuid

    Note: the PUUID must be from the summoner API. The
    current API token does not support the account API

    Args:
        puuid (str): the riot puuid (see riot developer docs)

    Returns:
        accoundId (str): the riot accountId associated with the
            given PUUID
    """
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    return riot_api_get(url)["accountId"]


def get_matches(account_id: str, start_timestamp: int):
    """"""
    url = f"https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?beginTime={start_timestamp}"
    response = riot_api_get(url)
    return [
        LoLMatchMetadata(item["gameId"], item["champion"], item["timestamp"])
        for item in response["matches"]
    ]


def get_match_data(match_id: int) -> Any:
    """
    Returns all the match data for a given match

    This returns information about the match, mainly
    overall statistics, team compositions and state of
    the match when it ended

    Args:
        match_id (int): the numeric identifier for a
            match (see riot developer docs)

    Returns:
        Any: the full json response from the riot API
    """
    url = f"https://na1.api.riotgames.com/lol/match/v4/matches/{match_id}"
    return riot_api_get(url)


def get_match_timeline(match_id: int) -> Any:
    """
    Returns a timeline of the match

    Args:
        match_id (int): the numeric identifier for the match

    Returns:
        Any: the full json response from the riot API
    """
    url = f"https://na1.api.riotgames.com/lol/match/v4/timelines/by-match/{match_id}"
    return riot_api_get(url)


def get_puuid(summoner_name: str) -> str:
    """
    Returns a riot puuid based on a summoner name

    Args:
        summoner_name (str): the name of the summoner
            to get a puuid for

    Returns:
        str: the puuid for the given summoner
    """

    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    return riot_api_get(url)["puuid"]
