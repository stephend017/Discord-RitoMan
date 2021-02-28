from typing import Dict, Union
from discord_ritoman.discord_api import send_discord_message
from discord_ritoman.db.schema import LoLUser
from discord_ritoman.lol.rules.lol_rule import lol_rule, LoLRuleType, LoLRule
from discord_ritoman.lol.stats.match_stat import get_stat


@lol_rule("trolled", LoLRuleType.GAME_END, run_after=["hard_inted", "inted"])
class TrolledRule(LoLRule):
    def should_run(
        self, results: Dict[str, bool], user: Union[LoLUser, None] = None
    ) -> bool:
        if get_stat("winner")["user"]:
            return False

        if results["hard_inted"] or results["inted"]:
            return False

        kills = get_stat("kills")
        deaths = get_stat("deaths")

        # should be true if 'inted' was false, just a double check :^)
        return kills["solo_kills"] >= deaths["solo_deaths"]

    def run(self, results: Dict[str, bool], user: Union[LoLUser, None] = None):
        send_discord_message(
            f"<@{user.discord_id}> got fucking trolled in their last game of league of legends. unlucky m8"
        )
