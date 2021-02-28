from discord_ritoman.discord_api import send_discord_message
from discord_ritoman.db.accessors import (
    get_lol_users_with_winrate_enabled,
    reset_all_lol_user_winrate,
)
from discord_ritoman.db.schema import LoLUser
from typing import Dict, List, Union
from discord_ritoman.lol.rules.lol_rule import LoLRule, LoLRuleType, lol_rule


@lol_rule("winrate-eod", LoLRuleType.END_OF_DAY)
class WinrateEODRule(LoLRule):
    def should_run(
        self, _results: Dict[str, bool], _user: Union[LoLUser, None] = None
    ) -> bool:
        # right now we always run this rule
        return True

    def run(
        self, _results: Dict[str, bool], _user: Union[LoLUser, None] = None
    ):
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
                    f"<@{user.discord_id}> fucking wasted their time today with {user.wins} wins and {user.losses} losses"
                )

            if user.wins < user.losses:  # only those who played
                send_discord_message(
                    f"<@{user.discord_id}> inted today with {user.wins} wins and {user.losses} losses. you fucked up, but im sure it was your team who trolled and not your fault"
                )

        if played_count == 0:
            send_discord_message(
                "Well fuck you little shits didn't play a single game. how sad."
            )

        reset_all_lol_user_winrate()
