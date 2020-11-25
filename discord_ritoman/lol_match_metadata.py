from fastcore.utils import store_attr
import json


class LoLMatchMetadata:
    """
    This class represents a League of Legends match by its metadata
    """

    def __init__(self, game_id: int, champion: int, timestamp: int):
        store_attr()

    def __str__(self) -> str:
        """"""
        return f"<{self.__class__.__name__} {[f'{key}={value}' for key, value in self.__dict__.items()]}>"

    def __repr__(self) -> str:
        """"""
        return f"<{self.__class__.__name__} {[f'{key}={value}' for key, value in self.__dict__.items()]}>"

    def __eq__(self, other) -> bool:
        if type(other) != type(self):
            return False

        return (
            self.game_id == other.game_id
            and self.champion == other.champion
            and self.timestamp == other.timestamp
        )

    def get_champion_name(self):
        """"""
        with open("./discord_ritoman/assets/champion.json", "r") as fp:
            champion_file = json.load(fp)
            for champion_name, champion_data in champion_file["data"].items():
                if int(champion_data["key"]) == self.champion:
                    return champion_name
        raise Exception(f"Unable to find champion with key={self.champion}")
