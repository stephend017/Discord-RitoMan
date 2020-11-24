from discord_ritoman.discord_api import send_discord_message
from typing import Any, Dict, List
from discord_ritoman.lol_match_metadata import LoLMatchMetadata
from discord_ritoman.db_api import (
    get_all_discord_users,
    get_all_prefixes,
    get_last_recorded_time,
    set_last_recorded_time,
    get_all_stat_prefixes_01,
    get_all_suffixes,
)
from discord_ritoman.lol_api import (
    get_account_id,
    get_matches,
    get_match_data,
    get_match_timeline,
)
from discord_ritoman.lol_match_data import LoLMatchData
import random
import logging

logger = logging.Logger("API Logger")
logger.addHandler(logging.FileHandler("./api.log"))


def handle_lol_loss(
    data, user_info, account_id, prefixes, stat_prefixes_01, suffixes, champion
):
    """"""
    solo_kills: int = data.get_solo_kills(account_id)
    solo_deaths: int = data.get_solo_killed(account_id)
    if solo_kills < solo_deaths:
        prefix_index: int = random.randint(0, len(prefixes) - 1)
        stat_prefix_01_index: int = random.randint(
            0, len(stat_prefixes_01) - 1
        )
        suffix_index: int = random.randint(0, len(suffixes) - 1)
        send_discord_message(
            f"{prefixes[prefix_index][0]} <@{user_info[2]}> {stat_prefixes_01[stat_prefix_01_index][0]} {solo_deaths} solo deaths and only {solo_kills} solo kills as {champion} in their latest defeat in league of legends. {suffixes[suffix_index][0]}"
        )


def handle_lol_match(
    match,
    account_id,
    user_info,
    timestamp,
    prefixes,
    stat_prefixes_01,
    suffixes,
):
    """"""
    match_data: Dict[str, Any] = {}
    match_timeline: Dict[str, Any] = {}

    try:
        match_data = get_match_data(match.game_id)
        match_timeline = get_match_timeline(match.game_id)
    except Exception:
        logger.error(
            "There was an error retrieving match data, skipping this iteration"
        )
        return

    data = LoLMatchData(match_data, match_timeline)
    champion = match.get_champion_name()

    # check if the user lost and had less solo kills
    # than solo deaths
    if not data.did_account_win(account_id):
        handle_lol_loss(
            data,
            user_info,
            account_id,
            prefixes,
            stat_prefixes_01,
            suffixes,
            champion,
        )

    match_end = data.get_match_end()
    if match_end > timestamp:
        set_last_recorded_time(user_info[0], data.get_match_end())


def run_lol():
    """
    This is the function that updates and sends messages
    to the discord server for every bad game
    """
    users = get_all_discord_users()
    prefixes = get_all_prefixes()
    stat_prefixes_01 = get_all_stat_prefixes_01()
    suffixes = get_all_suffixes()

    for user_info in users:
        timestamp = get_last_recorded_time(user_info[0])

        account_id: str = ""
        matches: List[LoLMatchMetadata] = []

        try:
            account_id = get_account_id(user_info[1])

        except Exception:
            logger.error(
                "There was an error retrieving account data, skipping this iteration"
            )
            continue

        try:
            matches = get_matches(account_id, timestamp)
        except Exception:
            logger.error(
                f"There was an error retrieving matches for account [{user_info[0]}], skipping this iteration"
            )
            continue

        for match in matches:
            handle_lol_match(
                match,
                account_id,
                user_info,
                timestamp,
                prefixes,
                stat_prefixes_01,
                suffixes,
            )
