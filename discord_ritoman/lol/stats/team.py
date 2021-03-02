from typing import Any, Dict
from discord_ritoman.lol.stats.match_stat import (
    LoLMatchStat,
    get_stat,
    lol_match_stat,
)


@lol_match_stat("team", requires=["participant_ids"])
class TeamStat(LoLMatchStat):
    """"""

    def process(
        self, data: Dict[str, Any], timeline: Dict[str, Any], account_id: str,
    ) -> Any:

        for participant in data["participants"]:
            if (
                participant["participantId"]
                == get_stat("participant_ids")[account_id]
            ):
                return participant["teamId"]
        return None
