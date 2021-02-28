from typing import Dict, Union
from discord_ritoman.discord_api import send_discord_message
from discord_ritoman.db.schema import LoLUser
from discord_ritoman.lol.rules.lol_rule import LoLRule, LoLRuleType, lol_rule
from discord_ritoman.lol.stats.match_stat import get_stat


@lol_rule("hard_inted", LoLRuleType.GAME_END)
class HardIntedRule(LoLRule):
    """"""

    def should_run(
        self, results: Dict[str, bool], user: Union[LoLUser, None] = None
    ) -> bool:
        """"""
        if get_stat("winner")["user"]:
            # user won game, cant have inted
            return False

        deaths = get_stat("deaths")

        return (
            deaths["max_deaths_to_champ"]["deaths"]
            >= deaths["total_deaths"] / 2
            and deaths["has_max_deaths"]
        )

    def run(self, results: Dict[str, bool], user: Union[LoLUser, None] = None):
        deaths = get_stat("deaths")
        champions = get_stat("champions")

        message = f"well well well, dinner has been served because <@{user.discord_id}> fed the absolute shit out of {champions[deaths['max_deaths_to_champ']['champ_id']]} giving them "

        # if max_solo_deaths_to_champ == solo_deaths:
        if deaths["max_deaths_to_champ"]["deaths"] == deaths["solo_deaths"]:
            message += f"all {deaths['max_deaths_to_champ']['deaths']} of their solo deaths"
        else:
            # message += f"{max_solo_deaths_to_champ} / {solo_deaths} of their solo deaths"
            message += f"{deaths['max_deaths_to_champ']['deaths']} / {deaths['solo_deaths']} of their solo deaths"

        send_discord_message(message, True)
