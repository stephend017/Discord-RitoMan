from typing import Any, Dict
from discord_ritoman.lol.stats.match_stat import (
    LoLMatchStat,
    get_stat,
    lol_match_stat,
)


@lol_match_stat("kills", requires=["participant_ids"])
class KillStat(LoLMatchStat):
    """"""

    def process(
        self, data: Dict[str, Any], timeline: Dict[str, Any], account_id: str,
    ) -> Any:
        participant_id = get_stat("participant_ids")[account_id]

        result: Any = {"total_kills": 0, "solo_kills": 0, "data": {}}

        for frame in timeline["frames"]:
            for event in frame["events"]:
                if event["type"] == "CHAMPION_KILL":
                    if event["killerId"] == participant_id:
                        result["total_kills"] += 1
                        if len(event["assistingParticipantIds"]) == 0:
                            result["solo_kills"] += 1

                        # handle kill data (used for feeding detection)
                        if event["victimId"] in result["data"]:
                            result["data"][event["victimId"]] += 1
                        else:
                            result["data"][event["victimId"]] = 1
        return result
