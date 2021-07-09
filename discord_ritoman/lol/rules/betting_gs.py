from discord_ritoman.utils import create_logger
from discord_ritoman.discord_api import send_discord_message
from discord_ritoman.db.schema import LoLUser
from typing import Dict, Optional
from discord_ritoman.lol.rules.lol_rule import LoLRule, LoLRuleType, lol_rule

logger = create_logger(__file__)


@lol_rule("betting-gs", LoLRuleType.GAME_START)
class BettingGSRule(LoLRule):
    def should_run(
        self, results: Dict[str, bool], user: Optional[LoLUser]
    ) -> bool:
        return True

    def run(self, results: Dict[str, bool], user: Optional[LoLUser]):
        logger.info(user)
        if user is None:
            return
        send_discord_message(
            f"<@{user.discord_id}> is ready to be hurt again. Time to place your bets."
        )
