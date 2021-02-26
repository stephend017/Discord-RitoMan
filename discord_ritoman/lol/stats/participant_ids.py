from typing import Any, Dict
from discord_ritoman.lol.stats.match_stat import LoLMatchStat, lol_match_stat


@lol_match_stat("participant_ids")
class ParticipantIdsStat(LoLMatchStat):
    """"""

    def process(
        self, data: Dict[str, Any], timeline: Dict[str, Any], account_id: str,
    ) -> Any:
        participant_ids = {}
        for participant in data["participantIdentities"]:
            participant_ids[participant["player"]["accountId"]] = participant[
                "participantId"
            ]
            if participant["player"]["accountId"] == account_id:
                participant_ids["user"] = participant["participantId"]
        return participant_ids
