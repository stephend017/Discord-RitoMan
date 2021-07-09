from discord_ritoman.discord_api import send_discord_message
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
            if better.created < get_stat("match_start"):
                # exclude bets placed after game started
                continue

            better_points.append(
                Casino.calculate_better_points(
                    better.amount,
                    did_win,
                    better.prediction,
                    GameMode.UNDEFINED,
                )
            )

        player_bonus = Casino.calculate_player_bonus(
            player_points, sum(better_points)
        )

        add_lol_user_points(user, int(player_bonus + player_points))

        player_result_message = f"<@{user.discord_id}> won {int(player_bonus + player_points)} points"
        betting_results_message = ""

        for better in betters:
            better_user = get_lol_user_by_discord_id(better.better)

            if better_user is None:
                continue

            better_point = Casino.calculate_better_points(
                better.amount, did_win, better.prediction, GameMode.UNDEFINED
            )
            better_bonus = Casino.calculate_better_bonus(
                player_points, better_point
            )

            add_lol_user_points(better_user, int(better_bonus + better_point))

            betting_results_message += f'<@{better.better}> {"won" if better.prediction == did_win else "lost"} their bet of {better.amount} and won a total of {int(better_bonus + better_point)}\n'
            remove_bet(better)

        send_discord_message(
            f"<@{user}> {'won' if did_win else 'lost'} their game of League which means that \n{betting_results_message}\n and finally\n {player_result_message}"
        )

        remove_lol_game(get_stat("game_id"), user.discord_id)
