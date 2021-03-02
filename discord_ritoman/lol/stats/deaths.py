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
            "max_deaths_to_champ": {"champ_id": 0, "deaths": 0},
        }

        td, sd, d = self._process_timeline(timeline, participant_id)
        result["total_deaths"] = td
        result["solo_deaths"] = sd
        result["data"] = d

        hmd = self._process_max_deaths(data, result["total_deaths"])
        result["has_max_deaths"] = hmd

        msd, c = self._process_participants(result["data"])
        result["max_deaths_to_champ"]["champ_id"] = c
        result["max_deaths_to_champ"]["deaths"] = msd

        return result

    def _process_timeline(self, timeline: Dict[str, Any], participant_id):
        total_deaths = 0
        solo_deaths = 0
        data = {}
        for frame in timeline["frames"]:
            for event in frame["events"]:
                if event["type"] == "CHAMPION_KILL":
                    if event["victimId"] == participant_id:
                        total_deaths += 1

                        if len(event["assistingParticipantIds"]) == 0:
                            solo_deaths += 1

                            # handle kill data (used for feeding detection)
                            if event["killerId"] in data:
                                data[event["killerId"]] += 1
                            else:
                                data[event["killerId"]] = 1
        return total_deaths, solo_deaths, data

    def _process_max_deaths(self, data, total_deaths):
        for participant in data["participants"]:
            if participant["teamId"] == get_stat("team"):
                if participant["stats"]["deaths"] > total_deaths:
                    return False
        return True

    def _process_participants(self, data):
        max_solo_deaths_to_champ = 0
        champ = 0
        for key, value in data.items():
            if value > max_solo_deaths_to_champ:
                champ = key
                max_solo_deaths_to_champ = value

        return max_solo_deaths_to_champ, champ
