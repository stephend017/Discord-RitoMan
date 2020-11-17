from typing import Any, Dict
from fastcore.utils import store_attr


class LoLMatchData:
    def __init__(self, data: Dict[str, Any], timeline: Dict[str, Any]):
        store_attr()

    def winning_team(self) -> int:
        """
        """
        for team in self.data["teams"]:
            if team["win"] == "Win":
                return team["teamId"]
        raise Exception("Failed to get winning team")

    def get_participant_id(self, account_id: str) -> int:
        """
        """
        for participant in self.data["participantIdentities"]:
            if participant["player"]["accountId"] == account_id:
                return participant["participantId"]
        raise Exception("Failed to get participantId")

    def did_account_win(self, account_id: int) -> bool:
        """
        """
        participant_id = self.get_participant_id(account_id)
        for participant in self.data["participants"]:
            if participant["participantId"] == participant_id:
                return participant["teamId"] == self.winning_team()
        raise Exception("Failed to determine if participant won")

    def get_solo_kills(self, account_id: int) -> int:
        """
        """
        participant_id = self.get_participant_id(account_id)
        count = 0
        for frame in self.timeline["frames"]:
            for event in frame["events"]:
                if event["type"] == "CHAMPION_KILL":
                    if event["killerId"] == participant_id:
                        if len(event["assistingParticipantIds"]) == 0:
                            count += 1
        return count

    def get_solo_killed(self, account_id: int) -> int:
        """
        """
        participant_id = self.get_participant_id(account_id)
        count = 0
        for frame in self.timeline["frames"]:
            for event in frame["events"]:
                if event["type"] == "CHAMPION_KILL":
                    if event["victimId"] == participant_id:
                        if len(event["assistingParticipantIds"]) == 0:
                            count += 1
        return count

    def get_match_end(self):
        """
        """
        return self.data["gameCreation"] + self.data["gameDuration"] * 1000
