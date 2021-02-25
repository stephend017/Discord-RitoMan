from typing import Any, Dict
from discord_ritoman.lol.stats.match_stat import (
    LoLMatchStat,
    get_stat,
    lol_match_stat,
)


@lol_match_stat("winner", requires=["participant_ids"])
class WinnerStat(LoLMatchStat):
    """"""

    def process(
        self, data: Dict[str, Any], timeline: Dict[str, Any], account_id: str,
    ) -> Any:
        participant_id = get_stat("participant_ids")[account_id]
        result = {}
        # compute winning team
        for team in data["teams"]:
            if team["win"] == "Win":
                result["team"] = team["teamId"]

        for participant in data["participants"]:
            if participant["participantId"] == participant_id:
                result["user"] = participant["teamId"] == result["team"]

        return result
