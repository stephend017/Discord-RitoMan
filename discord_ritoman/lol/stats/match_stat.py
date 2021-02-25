from typing import Any, Dict, List
from discord_ritoman.utils import create_logger

GLOBAL_MATCH_STATISTICS = {}
UNPROCESSED_STATS = {}
LOL_DATA_CONTEXT = {"data": None, "timeline": None, "account_id": None}


class LoLMatchStat:
    def process(
        self, data: Dict[str, Any], timeline: Dict[str, Any], account_id: str,
    ) -> Any:
        """
        function to compute a new stat

        Args:
            processed_stats (Dict[str, Any]): all stats that have been processed already
            data (Dict[str, Any]): The match metadata
            timeline (Dict[str, Any]): The match timeline data
            account_id (str): The riot puuid of the account that is being processed for

        Returns:
            Any: Value of this statistic
        """
        raise NotImplementedError

    def description(self):
        """
        Returns a description of this statistic. This should include
        what is calculated, what is required and how it can be used.
        """
        raise NotImplementedError


def set_lol_data_context(
    data: Dict[str, Any], timeline: Dict[str, Any], account_id: str
):
    """"""
    global LOL_DATA_CONTEXT
    LOL_DATA_CONTEXT["data"] = data
    LOL_DATA_CONTEXT["timeline"] = timeline
    LOL_DATA_CONTEXT["account_id"] = account_id


def reset_statistics():
    """"""
    global GLOBAL_MATCH_STATISTICS
    global UNPROCESSED_STATS

    for name, data in GLOBAL_MATCH_STATISTICS.items():
        UNPROCESSED_STATS[name] = data["w"]

    GLOBAL_MATCH_STATISTICS = {}
    update_unprocessed()


def can_process(wrapper_cls) -> bool:
    """
    Returns true if the stat can be processed false otherwise
    """
    for requirement in wrapper_cls.requires:
        if requirement not in GLOBAL_MATCH_STATISTICS:
            return False
    return True


def update_unprocessed():
    """
    updates all unprocessed stats
    """
    global GLOBAL_MATCH_STATISTICS
    global UNPROCESSED_STATS
    changed = False

    for name, stat in UNPROCESSED_STATS.items():
        if can_process(stat):
            del UNPROCESSED_STATS[name]
            GLOBAL_MATCH_STATISTICS[name] = {
                "value": stat.obj.process(
                    LOL_DATA_CONTEXT["data"],
                    LOL_DATA_CONTEXT["timeline"],
                    LOL_DATA_CONTEXT["account_id"],
                ),
                "w": stat,
            }
            changed = True
            break
    if changed:
        update_unprocessed()


def get_stat(name: str) -> Any:
    """"""
    if name in GLOBAL_MATCH_STATISTICS:
        return GLOBAL_MATCH_STATISTICS[name]["value"]

    if name in UNPROCESSED_STATS:
        raise ValueError(
            f"Stat [{name}] was registered but was not able to be processed due to outstanding dependencies"
        )

    raise ValueError(f"Unknown stat name [{name}]")


def lol_match_stat(name: str, requires: List[str] = []):
    """
    decorator for registering an lol match statistic
    """
    if name in GLOBAL_MATCH_STATISTICS:
        raise ValueError("statistic already defined")

    def decorator(cls):
        """
        This is a class decorator
        """
        if not issubclass(cls, LoLMatchStat):
            raise ValueError(
                "Cannot register class that does not extend LoLMatchStat"
            )

        global GLOBAL_MATCH_STATISTICS
        global UNPROCESSED_STATS

        class WrapperCls:
            def __init__(self, obj):
                self.obj = obj
                self.name = name
                self.requires = requires

        w = WrapperCls(cls())
        UNPROCESSED_STATS[name] = w

        return w

    return decorator
