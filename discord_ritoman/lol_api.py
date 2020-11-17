"""
this is the api for mypackage
"""
from discord_ritoman.lol_match_data import LoLMatchData
from discord_ritoman.db_api import get_all_discord_users
from typing import List
from discord_ritoman.lol_match_metadata import LoLMatchMetadata
import requests
import datetime
from discord_ritoman.utils import unix_time_millis
import os


RIOT_TOKEN = os.getenv(
    "RIOT_TOKEN", "RGAPI-a37a2689-066d-4fd2-80aa-257653241d65"
)


def get_account_id(puuid: str):
    """
    """
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": RIOT_TOKEN,
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()["accountId"]

    print(
        f"GET encrypted account ID request failed: [{response.status_code}] {response.text}"
    )
    raise Exception(
        f"GET encrypted account ID request failed: [{response.status_code}] {response.text}"
    )


def get_matches(account_id: str, start_timestamp: int):
    """
    """
    url = f"https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?beginTime={start_timestamp}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": RIOT_TOKEN,
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        return [
            LoLMatchMetadata(
                item["gameId"], item["champion"], item["timestamp"]
            )
            for item in response.json()["matches"]
        ]

    print(
        f"GET matches request failed: [{response.status_code}] {response.text}"
    )
    raise Exception(
        f"GET matches request failed: [{response.status_code}] {response.text}"
    )


def get_match_data(match_id: int):
    """
    """
    url = f"https://na1.api.riotgames.com/lol/match/v4/matches/{match_id}"
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
    raise Exception(
        f"GET match data request failed: [{response.status_code}] {response.text}"
    )


def get_match_timeline(match_id: int):
    """
    """
    url = f"https://na1.api.riotgames.com/lol/match/v4/timelines/by-match/{match_id}"
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
    raise Exception(
        f"GET match timeline request failed: [{response.status_code}] {response.text}"
    )
