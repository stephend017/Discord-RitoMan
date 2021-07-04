from typing import Any, Dict
from discord_ritoman.lol.stats.match_stat import LoLMatchStat, lol_match_stat


@lol_match_stat("game_id")
class GameIdStat(LoLMatchStat):
    """"""

    def process(
        self, data: Dict[str, Any], timeline: Dict[str, Any], account_id: str,
    ) -> Any:
        return data["gameId"]
