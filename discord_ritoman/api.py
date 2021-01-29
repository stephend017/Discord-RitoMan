from discord_ritoman.utils import create_logger
from discord_ritoman.models import GameResult
from discord_ritoman.discord_api import send_discord_message
from typing import Any, Dict, List
from discord_ritoman.lol_match_metadata import LoLMatchMetadata
from discord_ritoman.db_api import (
    add_new_lol_game,
    does_user_record_lol_winrate,
    get_all_discord_users,
    get_all_lol_users_winrate,
    get_all_prefixes,
    get_last_recorded_time,
    reset_all_lol_user_winrates,
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

# import logging
# from logging.handlers import RotatingFileHandler

# log_formatter = logging.Formatter(
#     "%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s"
# )

# logFile = "./api.log"

# my_handler = RotatingFileHandler(
#     logFile,
#     mode="a",
#     maxBytes=5 * 1024 * 1024,
#     backupCount=2,
#     encoding=None,
#     delay=0,
# )
# my_handler.setFormatter(log_formatter)
# my_handler.setLevel(logging.INFO)

# logger = logging.getLogger("api")
# logger.setLevel(logging.INFO)

# logger.addHandler(my_handler)

logger = create_logger(__file__)


def handle_lol_loss(
    data: LoLMatchData,
    user_info,
    account_id,
    prefixes,
    stat_prefixes_01,
    suffixes,
    champion,
):
    """"""
    logger.info("HANDLING LOL LOSS")
    solo_kills: int = data.get_solo_kills(account_id)
    solo_deaths: int = data.get_solo_killed(account_id)
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
            message = f"well well well, dinner has been served because <@{user_info[2]}> fed the absolute shit out of {data.get_champion_name_from_pariticpant_id(champ)} giving them "

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
                f"{prefixes[prefix_index][0]} <@{user_info[2]}> {stat_prefixes_01[stat_prefix_01_index][0]} {solo_deaths} solo deaths and only {solo_kills} solo kills as {champion} in their latest defeat in league of legends. {suffixes[suffix_index][0]}"
            )
        else:
            send_discord_message(
                f"<@{user_info[2]}> got fucking trolled in their last game of league of legends. unlucky m8"
            )
    except Exception as error:
        logger.critical(error)

    logger.info("FINISHED PROCESSING LOL LOSS DATA")


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

    logger.info("starting to load match data")

    data = LoLMatchData(match_data, match_timeline, account_id)
    champion = match.get_champion_name()

    logger.info("successfully loaded match data")

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
        if does_user_record_lol_winrate(user_info[0]):
            add_new_lol_game(user_info[0], GameResult.LOSS)
    else:
        if does_user_record_lol_winrate(user_info[0]):
            add_new_lol_game(user_info[0], GameResult.WIN)

    match_end = data.get_match_end()
    logger.info(f"{match_end} > {timestamp}")
    if match_end > timestamp:
        set_last_recorded_time(user_info[0], data.get_match_end())


def run_lol():
    """
    This is the function that updates and sends messages
    to the discord server for every bad game
    """
    logger.info("Starting lol run")
    users = get_all_discord_users()
    prefixes = get_all_prefixes()
    stat_prefixes_01 = get_all_stat_prefixes_01()
    suffixes = get_all_suffixes()

    logger.info(",".join(userinfo[0] for userinfo in users))

    for user_info in users:
        logger.info(f"processing user {user_info[0]}")
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


def dump_lol_winrate():
    """
    sends a discord message at 12 AM EST with the winrate
    for everyone who played that day
    """

    logger.info("starting winrate dump")
    users = get_all_lol_users_winrate()

    send_discord_message(
        "good evening degens, I'm here to glorify those who carried and shame those who inted"
    )

    for user in users:
        discord_id = user[0]
        wins = user[1]
        losses = user[2]
        if wins > losses:
            send_discord_message(
                f"<@{discord_id}> carried today with {wins} wins and {losses} losses, good job summoner"
            )
        else:
            send_discord_message(
                f"<@{discord_id}> inted today with {wins} wins and {losses} losses. you fucked up, but im sure it was your team who trolled and not your fault"
            )

    logger.info("wiping todays stats")
    reset_all_lol_user_winrates()
