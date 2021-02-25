import json
from typing import Any, Dict
from discord_ritoman.lol.stats.match_stat import LoLMatchStat, lol_match_stat


@lol_match_stat("champions")
class ChampionsStat(LoLMatchStat):
    """"""

    def process(
        self, data: Dict[str, Any], timeline: Dict[str, Any], account_id: str,
    ) -> Any:
        champions = {}
        with open("./discord_ritoman/assets/champion.json", "r") as fp:
            champion_file = json.load(fp)
            for participant in data["participants"]:
                champion_id = participant["championId"]
                for champion_name, champion_data in champion_file[
                    "data"
                ].items():
                    if champion_id == int(champion_data["key"]):
                        champions[participant["participantId"]] = champion_name
        return champions
