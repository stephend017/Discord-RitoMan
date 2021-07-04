from discord_ritoman.discord_api import send_discord_message
from discord_ritoman.db.schema import LoLUser
from typing import Dict, Union
from discord_ritoman.lol.rules.lol_rule import LoLRule, LoLRuleType, lol_rule


@lol_rule("betting-gs", LoLRuleType.GAME_START)
class BettingGSRule(LoLRule):
    def should_run(
        self, results: Dict[str, bool], user: Union[LoLUser, None]
    ) -> bool:
        return True

    def run(self, results: Dict[str, bool], user: Union[LoLUser, None]):
        if user is None:
            return
        send_discord_message(
            f"<@{user.discord_id}> is ready to be hurt again. Time to place your bets."
        )
