from discord_ritoman.db.schema import LoLText, LoLUser
from discord_ritoman.db.accessors import (
    get_all_lol_users,
    get_lol_text_by_group,
    get_lol_users_with_winrate_enabled,
    reset_all_lol_user_winrate,
    update_lol_user_last_updated,
    update_lol_user_winrate,
)
from discord_ritoman.utils import create_logger
from discord_ritoman.models import GameResult
from discord_ritoman.discord_api import send_discord_message
from typing import Any, Dict, List
from discord_ritoman.lol_match_metadata import LoLMatchMetadata
from discord_ritoman.lol_api import (
    get_account_id,
    get_matches,
    get_match_data,
    get_match_timeline,
)
from discord_ritoman.lol_match_data import LoLMatchData
import random

logger = create_logger(__file__)


def handle_lol_loss(
    data: LoLMatchData,
    user: LoLUser,
    prefixes: List[LoLText],
    stat_prefixes_01: List[LoLText],
    suffixes: List[LoLText],
    champion: str,
):
    """"""
    logger.info("HANDLING LOL LOSS")
    solo_kills: int = data.get_solo_kills()
    solo_deaths: int = data.get_solo_killed()
    kills, deaths = data.get_feeding_data()

    logger.info("LOADED LOL LOSS DATA")

    total_deaths = data.get_total_deaths()
    max_solo_deaths_to_champ = 0
    champ = 0
    for key, value in deaths.items():
        if value > max_solo_deaths_to_champ:
            champ = key
            max_solo_deaths_to_champ = value

    try:
        if (
            max_solo_deaths_to_champ >= total_deaths / 2
            and data.has_max_team_deaths()
        ):
            # message = f"well well well, dinner has been served because <@{user_info[2]}> fed the absolute shit out of {data.get_champion_name_from_pariticpant_id(champ)} giving them "
            message = f"well well well, dinner has been served because <@{user.discord_id}> fed the absolute shit out of {data.get_champion_name_from_pariticpant_id(champ)} giving them "

            if max_solo_deaths_to_champ == solo_deaths:
                message += (
                    f"all {max_solo_deaths_to_champ} of their solo deaths"
                )
            else:
                message += f"{max_solo_deaths_to_champ} / {solo_deaths} of their solo deaths"

            send_discord_message(message)
        elif solo_kills < solo_deaths:
            prefix_index: int = random.randint(0, len(prefixes) - 1)
            stat_prefix_01_index: int = random.randint(
                0, len(stat_prefixes_01) - 1
            )
            suffix_index: int = random.randint(0, len(suffixes) - 1)
            send_discord_message(
                # f"{prefixes[prefix_index][0]} <@{user_info[2]}> {stat_prefixes_01[stat_prefix_01_index][0]} {solo_deaths} solo deaths and only {solo_kills} solo kills as {champion} in their latest defeat in league of legends. {suffixes[suffix_index][0]}"
                f"{prefixes[prefix_index].content} <@{user.discord_id}> {stat_prefixes_01[stat_prefix_01_index].content} {solo_deaths} solo deaths and only {solo_kills} solo kills as {champion} in their latest defeat in league of legends. {suffixes[suffix_index].content}"
            )
        else:
            send_discord_message(
                # f"<@{user_info[2]}> got fucking trolled in their last game of league of legends. unlucky m8"
                f"<@{user.discord_id}> got fucking trolled in their last game of league of legends. unlucky m8"
            )
    except Exception as error:
        logger.critical(error)

    logger.info("FINISHED PROCESSING LOL LOSS DATA")


def handle_lol_match(
    match,
    account_id,
    user: LoLUser,
    timestamp,
    prefixes: List[LoLText],
    stat_prefixes_01: List[LoLText],
    suffixes: List[LoLText],
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

    logger.info("starting to load match data")

    data = LoLMatchData(match_data, match_timeline, account_id)
    champion = match.get_champion_name()

    logger.info("successfully loaded match data")

    # check if the user lost and had less solo kills
    # than solo deaths
    if not data.did_account_win(account_id):
        handle_lol_loss(
            data, user, prefixes, stat_prefixes_01, suffixes, champion,
        )
        if user.winrate:
            update_lol_user_winrate(user, GameResult.LOSS)
    else:
        if user.winrate:
            update_lol_user_winrate(user, GameResult.WIN)

    match_end = data.get_match_end()
    logger.info(f"{match_end} > {timestamp}")
    if match_end > timestamp:
        # set_last_recorded_time(user_info[0], data.get_match_end())
        update_lol_user_last_updated(user, match_end)


def run_lol():
    """
    This is the function that updates and sends messages
    to the discord server for every bad game
    """
    logger.info("Starting lol run")
    users: List[LoLUser] = get_all_lol_users()
    prefixes: List[LoLText] = get_lol_text_by_group("p0")
    stat_prefixes_01: List[LoLText] = get_lol_text_by_group("sp0")
    suffixes: List[LoLText] = get_lol_text_by_group("s0")

    for user in users:
        timestamp = user.last_updated
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
            matches = get_matches(account_id, timestamp)
        except Exception:
            logger.error(
                f"There was an error retrieving matches for account [{user.discord_id}], skipping this iteration"
            )
            continue

        for match in matches:
            handle_lol_match(
                match,
                account_id,
                user,
                timestamp,
                prefixes,
                stat_prefixes_01,
                suffixes,
            )


def dump_lol_winrate():
    """
    sends a discord message at 7 PM EST with the winrate
    for everyone who played that day
    """

    logger.info("starting winrate dump")
    # users = get_all_lol_users_winrate()
    users: List[LoLUser] = get_lol_users_with_winrate_enabled()

    send_discord_message(
        "good evening degens, I'm here to glorify those who carried and shame those who inted"
    )

    played_count: int = 0

    for user in users:
        if user.wins == 0 and user.losses == 0:
            # skip users that dont play
            continue

        played_count += 1
        if user.wins > user.losses:
            send_discord_message(
                f"<@{user.discord_id}> carried today with {user.wins} wins and {user.losses} losses, good job summoner"
            )

        if user.wins == user.losses:
            send_discord_message(
                f"<@{user.discord_id}> fucking wasted their time today with {user.wins} wins and losses"
            )

        if user.wins < user.losses:  # only those who played
            send_discord_message(
                f"<@{user.discord_id}> inted today with {user.wins} wins and {user.losses} losses. you fucked up, but im sure it was your team who trolled and not your fault"
            )

    if played_count == 0:
        send_discord_message(
            "Well fuck you little shits didn't play a single game. how sad."
        )

    logger.info("wiping todays stats")
    reset_all_lol_user_winrate()
