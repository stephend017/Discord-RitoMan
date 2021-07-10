from discord_ritoman.lol.rules.lol_rule import LoLRuleType, run_lol_rules
from discord_ritoman.lol.stats.match_stat import (
    reset_statistics,
    set_lol_data_context,
)
from discord_ritoman.db.schema import LoLUser
from discord_ritoman.db.accessors import (
    add_lol_game,
    get_all_active_games,
    get_all_lol_users,
)
from discord_ritoman.utils import create_logger, with_logging
from typing import Any, Dict, List
from discord_ritoman.lol_match_metadata import (
    LoLMatchMetadata,
    LoLMatchStartData,
)
from discord_ritoman.lol_api import (
    get_account_id,
    get_active_game,
    get_encrypted_summoner_id,
    get_matches,
    get_match_data,
    get_match_timeline,
)

logger = create_logger(__file__)


def run_end_of_day():
    """
    Runs all the rules that have been defined to run at the end of the day

    See `discord_ritoman.lol.rules` for more info
    """
    run_lol_rules(LoLRuleType.END_OF_DAY)


def run_end_of_game(
    user: LoLUser,
    match_data: Dict[str, Any],
    match_timeline: Dict[str, Any],
    account_id: str,
):
    """
    Runs all the rules that have been defined to run at the end of each game

    Args:
        user (LoLUser): the user who's game ended
        match_data (Dict[str, Any]): the match data from the users game
            that ended
        match_timeline (Dict[str, Any]): the match timeline from the
            users game that ended
        account_id (str): the RIOT account id of the user
    """
    set_lol_data_context(match_data, match_timeline, account_id)
    reset_statistics()
    run_lol_rules(LoLRuleType.GAME_END, user)


def _poll_game_end():
    """
    Function that polls the LoL API checking for games
    that have ended for each user
    """
    users: List[LoLUser] = get_all_lol_users()

    for user in users:
        account_id: str = ""
        matches: List[LoLMatchMetadata] = []

        account_id = with_logging(
            get_account_id,
            logger,
            f"Failed to get account id for user=[{user.riot_puuid}]",
            None,
            puuid=user.riot_puuid,
        )

        if account_id is None:
            continue

        matches: List[LoLMatchMetadata] = with_logging(
            get_matches,
            logger,
            f"Failed to get matches for user=[{user.discord_id}]",
            [],
            account_id=account_id,
            start_timestamp=user.last_updated,
        )

        for match in matches:
            match_data = with_logging(
                get_match_data,
                logger,
                f"Failed to get match data for match=[{match.game_id}]",
                None,
                match_id=match.game_id,
            )

            match_timeline = with_logging(
                get_match_timeline,
                logger,
                f"Failed to get match timeline for match=[{match.game_id}]",
                None,
                match_id=match.game_id,
            )

            if match_data is None or match_timeline is None:
                continue

            run_end_of_game(user, match_data, match_timeline, account_id)


def _poll_game_start():
    """
    Function that polls the LoL API checking for games
    that have started for each user
    """
    users: List[LoLUser] = get_all_lol_users()
    # active_games = get_all_active_games()

    for user in users:
        game: LoLMatchStartData = with_logging(
            get_active_game,
            logger,
            f"Failed to get matches for user=[{user.discord_id}]",
            None,
            encrypted_summoner_id=get_encrypted_summoner_id(user.riot_puuid),
        )

        if game is None:
            continue

        # if (
        #     len(
        #         list(filter(lambda x: x.game_id == game.game_id, active_games))
        #     )
        #     > 0
        # ):
        #     # game_id already exists
        #     if (
        #         len(
        #             list(
        #                 filter(
        #                     lambda x: x.player == user.discord_id, active_games
        #                 )
        #             )
        #         )
        #         > 0
        #     ):
        #         # player already exists
        #         logger.info(
        #             f"games: {''.join(str(x) for x in active_games)} player: {user.discord_id}"
        #         )
        #         continue

        # player or game does not exist, create new entry
        add_lol_game(user, game.game_id, game.start_time, game.game_mode)

        run_lol_rules(LoLRuleType.GAME_START, user)


def poll_lol_api():
    """
    This function polls for 2 different events
    - Game ending
    - Game starting
    """
    _poll_game_end()
    _poll_game_start()
