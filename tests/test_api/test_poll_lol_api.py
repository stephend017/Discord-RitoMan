from discord_ritoman.lol_match_metadata import LoLMatchMetadata
from discord_ritoman.lol_api import (
    get_account_id,
    get_match_data,
    get_match_timeline,
    get_matches,
)
from typing import Any, Dict, List
from discord_ritoman.db.schema import LoLUser
import discord_ritoman.api
from discord_ritoman.api import poll_lol_api
from unittest import mock


def run_poll_lol_api(
    users: List[LoLUser] = [LoLUser(1, "p1")],
    with_logging_calls: Dict[Any, Any] = {},
):
    def decorator(func):
        @mock.patch.object(discord_ritoman.api, "run_end_of_day")
        @mock.patch.object(discord_ritoman.api, "with_logging")
        @mock.patch.object(discord_ritoman.api, "get_all_lol_users")
        def wrapper(
            mock_get_all_lol_users, mock_with_logging, mock_run_end_of_day
        ):
            def with_logging_handler(
                func, logger, log_message, default, **kwargs
            ):
                # validate other parameters here (if wanted)
                return with_logging_calls[func]

            mock_get_all_lol_users.return_value = users
            mock_with_logging.side_effect = with_logging_handler

            poll_lol_api()
            func(mock_run_end_of_day, users)

        return wrapper

    return decorator


@run_poll_lol_api(
    with_logging_calls={
        get_account_id: "A1",
        get_matches: [LoLMatchMetadata(11, 12, 13)],
        get_match_data: {"data": "value"},
        get_match_timeline: {"timeline": "value"},
    }
)
def test_poll_lol_api(mock_run_end_of_day, users):
    """"""
    for user in users:
        mock_run_end_of_day.assert_called_once_with(
            user, {"data": "value"}, {"timeline": "value"}, "A1"
        )
