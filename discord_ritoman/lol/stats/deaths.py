from typing import Any, Dict
from discord_ritoman.lol.stats.match_stat import (
    LoLMatchStat,
    get_stat,
    lol_match_stat,
)


@lol_match_stat("deaths", requires=["participant_ids", "team"])
class DeathStat(LoLMatchStat):
    """"""

    def process(
        self, data: Dict[str, Any], timeline: Dict[str, Any], account_id: str,
    ) -> Any:
        participant_id = get_stat("participant_ids")[account_id]

        result = {
            "total_deaths": 0,
            "solo_deaths": 0,
            "data": {},
            "has_max_deaths": True,
        }

        for frame in timeline["frames"]:
            for event in frame["events"]:
                if event["type"] == "CHAMPION_KILL":
                    if event["victimId"] == participant_id:
                        result["total_deaths"] += 1

                        if len(event["assistingParticipantIds"]) == 0:
                            result["solo_deaths"] += 1

                            # handle kill data (used for feeding detection)
                            if event["killerId"] in result["data"]:
                                result["data"][event["killerId"]] += 1
                            else:
                                result["data"][event["killerId"]] = 1

        for participant in data["participants"]:
            if participant["teamId"] == get_stat("team"):
                if participant["stats"]["deaths"] > result["total_deaths"]:
                    result["has_max_deaths"] = False

        return result
