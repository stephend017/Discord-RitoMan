from discord_ritoman.lol.stats.match_stat import get_stat
from discord_ritoman.models import GameResult
from discord_ritoman.db.schema import LoLUser
from typing import Dict, Union
from discord_ritoman.lol.rules.lol_rule import LoLRule, LoLRuleType, lol_rule
from discord_ritoman.db.accessors import update_lol_user_winrate


@lol_rule("winrate-ge", LoLRuleType.GAME_END)
class WinrateGERule(LoLRule):
    def should_run(
        self, results: Dict[str, bool], user: Union[LoLUser, None]
    ) -> bool:
        return user.winrate

    def run(self, results: Dict[str, bool], user: Union[LoLUser, None]):
        if not get_stat("winner")["user"]:
            update_lol_user_winrate(user, GameResult.LOSS)
        else:
            update_lol_user_winrate(user, GameResult.WIN)
