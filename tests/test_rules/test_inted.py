from tests.mock.discord_mocks import mock_discord_id
from discord_ritoman.db.schema import LoLText, LoLUser
from discord_ritoman.lol.stats.match_stat import (
    reset_statistics,
    set_lol_data_context,
)
from tests.mock.mock_match_data import (
    get_mock_match_data,
    get_mock_match_data_account_id,
    get_mock_match_timeline,
)
import discord_ritoman.lol.rules.inted
from unittest import mock
from discord_ritoman.lol.rules.inted import IntedRule


def should_run(
    solo_deaths: int = 12,
    solo_kills: int = 10,
    win: bool = False,
    hard_inted: bool = False,
):
    def decorator(func):
        @mock.patch.object(discord_ritoman.lol.rules.inted, "get_stat")
        def wrapper(mock_get_stat):

            match_data = get_mock_match_data()
            match_timeline = get_mock_match_timeline()

            set_lol_data_context(
                match_data, match_timeline, get_mock_match_data_account_id()
            )
            reset_statistics()

            stat_table = {
                "kills": {
                    "solo_kills": solo_kills,
                    "total_kills": 0,
                    "data": {},
                },
                "deaths": {
                    "solo_deaths": solo_deaths,
                    "total_deaths": 15,
                    "data": {0: 0, 1: 0},
                    "has_max_deaths": True,
                    "max_deaths_to_champ": {"champ_id": 1, "deaths": 0},
                },
                "champions": {1: "MasterLi", 0: "AnotherBitch"},
                "winner": {"user": win, "team": 100},
            }

            mock_get_stat.side_effect = lambda x: stat_table[x]

            user = LoLUser(mock_discord_id(), "useless")

            inted = IntedRule
            response = inted.obj.should_run({"hard_inted": hard_inted}, user)

            func(response)

        return wrapper

    return decorator


def run(
    solo_deaths: int = 12, solo_kills: int = 10,
):
    def decorator(func):
        @mock.patch.object(
            discord_ritoman.lol.rules.inted, "get_lol_text_by_group"
        )
        @mock.patch.object(
            discord_ritoman.lol.rules.inted, "send_discord_message"
        )
        @mock.patch.object(discord_ritoman.lol.rules.inted, "get_stat")
        def wrapper(
            mock_get_stat,
            mock_send_discord_message,
            mock_get_lol_text_by_group,
        ):

            match_data = get_mock_match_data()
            match_timeline = get_mock_match_timeline()

            set_lol_data_context(
                match_data, match_timeline, get_mock_match_data_account_id()
            )
            reset_statistics()

            stat_table = {
                "kills": {
                    "solo_kills": solo_kills,
                    "total_kills": 0,
                    "data": {},
                },
                "participant_ids": {
                    get_mock_match_data_account_id(): 1,
                    "user": 1,
                },
                "deaths": {
                    "solo_deaths": solo_deaths,
                    "total_deaths": 15,
                    "data": {0: 0, 1: 0},
                    "has_max_deaths": True,
                    "max_deaths_to_champ": {"champ_id": 1, "deaths": 0},
                },
                "champions": {1: "MasterLi", 0: "AnotherBitch"},
                "winner": {"user": False, "team": 100},
            }

            mock_get_stat.side_effect = lambda x: stat_table[x]

            user = LoLUser(mock_discord_id(), "useless")

            text_table = {
                "p0": [LoLText("p", "prefix", 1234)],
                "sp0": [LoLText("sp", "stat_prefix", 1234)],
                "s0": [LoLText("s", "suffix", 1234)],
            }

            mock_get_lol_text_by_group.side_effect = lambda x: text_table[x]

            inted = IntedRule
            inted.obj.run({"hard_inted": False}, user)

            func(mock_send_discord_message)

        return wrapper

    return decorator


@should_run()
def test_should_run(response):
    """"""
    assert response


@should_run(solo_deaths=0)
def test_should_run_no_deaths(response):
    """"""
    assert not response


@should_run(win=True)
def test_should_run_win(response):
    """"""
    assert not response


@should_run(hard_inted=True)
def test_should_run_hard_inted_ran(response):
    """"""
    assert not response


@run()
def test_run(mock_send_discord):
    """"""
    mock_send_discord.assert_called_once_with(
        f"prefix <@{mock_discord_id()}> stat_prefix 12 solo deaths and only 10 solo kills as MasterLi in their latest defeat in league of legends. suffix",
        True,
    )
