from discord_ritoman.db.accessors import (
    add_lol_user_points,
    get_betters_on,
    get_lol_user_by_discord_id,
    remove_bet,
    remove_lol_game,
)
from discord_ritoman.models import GameMode
from discord_ritoman.casino import Casino
from discord_ritoman.lol.stats.match_stat import get_stat
from discord_ritoman.db.schema import LoLUser
from typing import Dict, List, Union
from discord_ritoman.lol.rules.lol_rule import LoLRule, LoLRuleType, lol_rule


@lol_rule("betting-ge", LoLRuleType.GAME_END)
class BettingGERule(LoLRule):
    def should_run(
        self, results: Dict[str, bool], user: Union[LoLUser, None]
    ) -> bool:
        if user is None:
            return False
        return True

    def run(self, results: Dict[str, bool], user: Union[LoLUser, None]):
        if user is None:
            return
        did_win: bool = get_stat("winner")["user"]

        player_points = Casino.calculate_player_points(
            get_stat("takedowns"), did_win, GameMode.UNDEFINED
        )

        betters = get_betters_on(user)

        if len(betters) == 0:
            add_lol_user_points(user, int(player_points))
            return

        better_points: List[int] = []
        for better in betters:
            better_points.append(
                Casino.calculate_better_points(
                    better.amount,
                    did_win,
                    better.prediction,
                    GameMode.UNDEFINED,
                )
            )

        player_multiplier = Casino.calculate_player_multiplier(
            player_points, sum(better_points)
        )

        add_lol_user_points(user, int(player_multiplier * player_points))

        for better in betters:
            better_user = get_lol_user_by_discord_id(better.better)

            if better_user is None:
                continue

            better_point = Casino.calculate_better_points(
                better.amount, did_win, better.prediction, GameMode.UNDEFINED
            )
            better_multiplier = Casino.calculate_better_multiplier(
                player_points, better_point
            )

            add_lol_user_points(
                better_user, int(better_multiplier * better_point)
            )

            remove_bet(better)

        remove_lol_game(get_stat("game_id"), user.discord_id)
