import json
from typing import Any, Dict, Tuple
from fastcore.utils import store_attr


class LoLMatchData:
    def __init__(
        self, data: Dict[str, Any], timeline: Dict[str, Any], account_id: str
    ):
        store_attr()
        self.kill_data = {}
        self.kill_data["kills"] = {}
        self.kill_data["deaths"] = {}
        self.kill_data["solo_kills"] = 0
        self.kill_data["solo_deaths"] = 0
        self.kill_data["total_kills"] = 0
        self.kill_data["total_deaths"] = 0
        self._process_deaths(account_id)

    def winning_team(self) -> int:
        """"""
        for team in self.data["teams"]:
            if team["win"] == "Win":
                return team["teamId"]
        raise Exception("Failed to get winning team")

    def get_participant_id(self, account_id: str) -> int:
        """"""
        for participant in self.data["participantIdentities"]:
            if participant["player"]["accountId"] == account_id:
                return participant["participantId"]
        raise Exception("Failed to get participantId")

    def get_team_id(self):
        """
        returns the teamId of this user
        """
        participant_id = self.get_participant_id(self.account_id)
        for participant in self.data["participants"]:
            if participant["participantId"] == participant_id:
                return participant["teamId"]

    def did_account_win(self, account_id: str) -> bool:
        """"""
        # TODO refactor with code above
        participant_id = self.get_participant_id(account_id)
        for participant in self.data["participants"]:
            if participant["participantId"] == participant_id:
                return participant["teamId"] == self.winning_team()
        raise Exception("Failed to determine if participant won")

    def get_solo_kills(self, account_id: str) -> int:
        """"""
        return self.kill_data["solo_kills"]

    def get_solo_killed(self, account_id: str) -> int:
        """"""
        return self.kill_data["solo_deaths"]

    def get_total_kills(self):
        """"""
        return self.kill_data["total_kills"]

    def get_total_deaths(self):
        """"""
        return self.kill_data["total_deaths"]

    def get_match_end(self):
        """"""
        return self.data["gameCreation"] + self.data["gameDuration"] * 1000

    def get_feeding_data(self) -> Tuple[Dict[int, int], Dict[int, int]]:
        """
        Returns a tuple of dictionaries. the first dictionary contains data on who fed
        you and the second dictionary contains data on who you fed.

        In both dictionaries the key is the participant id of the other player and the
        value is the number of kills or deaths respectively
        """
        who_fed_me = {}
        who_i_fed = {}

        for key, value in self.kill_data["kills"].items():
            if key in self.kill_data["deaths"]:
                if value > self.kill_data["deaths"][key]:
                    who_fed_me[key] = value
                else:
                    who_i_fed[key] = self.kill_data["deaths"][key]
            else:
                # only deaths didnt die (this is a good thing)
                who_fed_me[key] = value

        # handle reverse case (i deaths zero people, yikes)
        for key, value in self.kill_data["deaths"].items():
            if key in self.kill_data["kills"]:
                # already handled from above
                continue

            # this is bad case (you fed really hard)
            who_i_fed[key] = value

        return who_fed_me, who_i_fed

    def get_champion_name_from_pariticpant_id(
        self, participant_id: int
    ) -> int:
        """
        returns a champion id from a participant id
        """
        champion_id = -1
        for participant in self.data["participants"]:
            if participant["participantId"] == participant_id:
                champion_id = participant["championId"]
                break

        with open("./discord_ritoman/assets/champion.json", "r") as fp:
            champion_file = json.load(fp)
            for champion_name, champion_data in champion_file["data"].items():
                if champion_id == int(champion_data["key"]):
                    return champion_name
        raise Exception(f"Unable to find champion with key={champion_id}")

    def has_max_team_deaths(self):
        """
        Returns true if this user has the most deaths on their team, false otherwise
        """
        teamId = self.get_team_id()
        max_deaths = self.kill_data["total_deaths"]
        for participant in self.data["participants"]:
            if (
                participant["teamId"] == teamId
                and participant["stats"]["deaths"] > max_deaths
            ):
                return False
        return True

    def _process_kill_data(self, account_id: str):
        """
        processes kill data for this user
        """
        self._process_kills(account_id)
        self._process_deaths(account_id)

    def _process_kills(self, account_id: str):
        """
        processes all kills made by this account
        """
        participant_id = self.get_participant_id(account_id)
        for frame in self.timeline["frames"]:
            for event in frame["events"]:
                if event["type"] == "CHAMPION_KILL":
                    if event["killerId"] == participant_id:
                        self.kill_data["total_kills"] += 1
                        if len(event["assistingParticipantIds"]) == 0:
                            self.kill_data["solo_kills"] += 1

                            # handle kill data (used for feeding detection)
                            if event["victimId"] in self.kill_data["kills"]:
                                self.kill_data["kills"][event["victimId"]] += 1
                            else:
                                self.kill_data["kills"][event["victimId"]] = 1

    def _process_deaths(self, account_id: str):
        """
        processes all deaths made by this account
        """
        participant_id = self.get_participant_id(account_id)
        for frame in self.timeline["frames"]:
            for event in frame["events"]:
                if event["type"] == "CHAMPION_KILL":
                    if event["victimId"] == participant_id:
                        self.kill_data["total_deaths"] += 1

                        if len(event["assistingParticipantIds"]) == 0:
                            self.kill_data["solo_deaths"] += 1

                            # handle kill data (used for feeding detection)
                            if event["killerId"] in self.kill_data["deaths"]:
                                self.kill_data["deaths"][
                                    event["killerId"]
                                ] += 1
                            else:
                                self.kill_data["deaths"][event["killerId"]] = 1
