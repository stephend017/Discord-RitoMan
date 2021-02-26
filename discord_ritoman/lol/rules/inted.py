from discord_ritoman.db.accessors import get_lol_text_by_group
from discord_ritoman.discord_api import send_discord_message
import random
from discord_ritoman.lol.stats.match_stat import get_stat
from typing import Dict, List
from discord_ritoman.db.schema import LoLText, LoLUser
from discord_ritoman.lol.rules.lol_rule import lol_rule, LoLRuleType, LoLRule


@lol_rule("inted", LoLRuleType.GAME_END, run_after=["hard_inted"])
class IntedRule(LoLRule):
    def should_run(self, results: Dict[str, bool], user: LoLUser) -> bool:
        if get_stat("winner")["user"]:
            return False

        if results["hard_inted"]:
            # dont run if hard inted ran
            return False

        kills = get_stat("kills")
        deaths = get_stat("deaths")

        return kills["solo_kills"] < deaths["solo_deaths"]

    def run(self, results: Dict[str, bool], user: LoLUser):
        kills = get_stat("kills")
        deaths = get_stat("deaths")
        champions = get_stat("champions")
        user_participant_id = get_stat("participant_ids")["user"]

        prefixes: List[LoLText] = get_lol_text_by_group("p0")
        stat_prefixes_01: List[LoLText] = get_lol_text_by_group("sp0")
        suffixes: List[LoLText] = get_lol_text_by_group("s0")

        prefix_index: int = random.randint(0, len(prefixes) - 1)
        stat_prefix_01_index: int = random.randint(
            0, len(stat_prefixes_01) - 1
        )
        suffix_index: int = random.randint(0, len(suffixes) - 1)

        send_discord_message(
            f"{prefixes[prefix_index].content} <@{user.discord_id}> {stat_prefixes_01[stat_prefix_01_index].content} {deaths['solo_deaths']} solo deaths and only {kills['solo_kills']} solo kills as {champions[user_participant_id]} in their latest defeat in league of legends. {suffixes[suffix_index].content}",
            True,
        )
