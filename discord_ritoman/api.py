from discord_ritoman.lol.rules.lol_rule import LoLRuleType, run_lol_rules
from discord_ritoman.lol.stats.match_stat import (
    reset_statistics,
    set_lol_data_context,
)
from discord_ritoman.db.schema import LoLUser
from discord_ritoman.db.accessors import get_all_lol_users
from discord_ritoman.utils import create_logger
from typing import Any, Dict, List
from discord_ritoman.lol_match_metadata import LoLMatchMetadata
from discord_ritoman.lol_api import (
    get_account_id,
    get_matches,
    get_match_data,
    get_match_timeline,
)

logger = create_logger(__file__)


def handle_lol_match(
    match: LoLMatchMetadata, account_id: str, user: LoLUser,
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

    set_lol_data_context(match_data, match_timeline, account_id)
    reset_statistics()

    # check if the user lost and had less solo kills
    # than solo deaths

    run_lol_rules(LoLRuleType.GAME_END, user)


def run_lol():
    """
    This is the function that updates and sends messages
    to the discord server for every bad game
    """
    users: List[LoLUser] = get_all_lol_users()

    for user in users:
        account_id: str = ""
        matches: List[LoLMatchMetadata] = []

        try:
            account_id = get_account_id(user.riot_puuid)
        except Exception:
            logger.error(
                "There was an error retrieving account data, skipping this iteration"
            )
            continue

        try:
            matches = get_matches(account_id, user.last_updated)
        except Exception:
            logger.error(
                f"There was an error retrieving matches for account [{user.discord_id}], skipping this iteration"
            )
            continue

        for match in matches:
            handle_lol_match(
                match, account_id, user,
            )


def dump_lol_winrate():
    """
    sends a discord message at 7 PM EST with the winrate
    for everyone who played that day
    """
    run_lol_rules(LoLRuleType.END_OF_DAY)
