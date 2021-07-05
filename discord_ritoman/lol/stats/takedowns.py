from typing import Any, Dict
from discord_ritoman.lol.stats.match_stat import (
    LoLMatchStat,
    get_stat,
    lol_match_stat,
)


@lol_match_stat("takedowns", requires=["participant_ids"])
class TakedownStat(LoLMatchStat):
    """"""

    def process(
        self, data: Dict[str, Any], timeline: Dict[str, Any], account_id: str,
    ) -> Any:
        participant_id = get_stat("participant_ids")[account_id]

        result = 0

        for participant in data["participants"]:
            if participant["participantId"] == participant_id:
                result = (
                    participant["stats"]["kills"]
                    + participant["stats"]["assists"]
                )
        return result
