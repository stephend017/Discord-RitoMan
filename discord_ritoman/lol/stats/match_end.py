from typing import Any, Dict
from discord_ritoman.lol.stats.match_stat import LoLMatchStat, lol_match_stat


@lol_match_stat("match_end")
class MatchEndStat(LoLMatchStat):
    """"""

    def process(
        self, data: Dict[str, Any], timeline: Dict[str, Any], account_id: str,
    ) -> Any:
        return data["gameCreation"] + data["gameDuration"] * 1000
