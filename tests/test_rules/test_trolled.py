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
import discord_ritoman.lol.rules.trolled
from unittest import mock
from discord_ritoman.lol.rules.trolled import TrolledRule


def should_run(
    solo_deaths: int = 10,
    solo_kills: int = 12,
    win: bool = False,
    hard_inted: bool = False,
    inted: bool = False,
):
    def decorator(func):
        @mock.patch.object(discord_ritoman.lol.rules.trolled, "get_stat")
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

            trolled = TrolledRule
            response = trolled.obj.should_run(
                {"hard_inted": hard_inted, "inted": inted}, user
            )

            func(response)

        return wrapper

    return decorator


def run():
    def decorator(func):
        @mock.patch.object(
            discord_ritoman.lol.rules.trolled, "send_discord_message"
        )
        def wrapper(mock_send_discord_message,):
            user = LoLUser(mock_discord_id(), "useless")

            trolled = TrolledRule
            trolled.obj.run({"hard_inted": False, "inted": False}, user)

            func(mock_send_discord_message)

        return wrapper

    return decorator


@should_run()
def test_should_run(response):
    """"""
    assert response


@should_run(solo_deaths=13)
def test_should_run_deaths_gt_kills(response):
    """"""
    assert not response


@should_run(hard_inted=True)
def test_should_run_hard_inted(response):
    """"""
    assert not response


@should_run(inted=True)
def test_should_run_inted(response):
    """"""
    assert not response


@run()
def test_run(mock_send_discord_message):
    """"""
    mock_send_discord_message.assert_called_once_with(
        f"<@{mock_discord_id()}> got fucking trolled in their last game of league of legends. unlucky m8"
    )
