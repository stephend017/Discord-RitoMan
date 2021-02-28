from tests.mock.discord_mocks import mock_discord_id
from discord_ritoman.db.schema import LoLUser
from discord_ritoman.lol.stats.match_stat import (
    reset_statistics,
    set_lol_data_context,
)
from tests.mock.mock_match_data import (
    get_mock_match_data,
    get_mock_match_data_account_id,
    get_mock_match_timeline,
)
import discord_ritoman.lol.rules.hard_inted
from unittest import mock
from discord_ritoman.lol.rules.hard_inted import HardIntedRule


def should_run(
    solo_deaths: int = 12,
    single_champ_solo_deaths: int = 10,
    win: bool = False,
):
    def decorator(func):
        @mock.patch.object(discord_ritoman.lol.rules.hard_inted, "get_stat")
        def wrapper(mock_get_stat):

            match_data = get_mock_match_data()
            match_timeline = get_mock_match_timeline()

            set_lol_data_context(
                match_data, match_timeline, get_mock_match_data_account_id()
            )
            reset_statistics()

            stat_table = {
                "kills": {"solo_kills": 0, "total_kills": 0, "data": {}},
                "deaths": {
                    "solo_deaths": solo_deaths,
                    "total_deaths": 15,
                    "data": {0: 0, 1: single_champ_solo_deaths},
                    "has_max_deaths": True,
                    "max_deaths_to_champ": {
                        "champ_id": 1,
                        "deaths": single_champ_solo_deaths,
                    },
                },
                "champions": {1: "MasterLi", 0: "AnotherBitch"},
                "winner": {"user": win, "team": 100},
            }

            mock_get_stat.side_effect = lambda x: stat_table[x]

            user = LoLUser(mock_discord_id(), "useless")

            hard_inted = HardIntedRule
            response = hard_inted.obj.should_run({}, user)

            func(response)

        return wrapper

    return decorator


def run(
    solo_deaths: int = 12, single_champ_solo_deaths: int = 10,
):
    def decorator(func):
        @mock.patch.object(
            discord_ritoman.lol.rules.hard_inted, "send_discord_message"
        )
        @mock.patch.object(discord_ritoman.lol.rules.hard_inted, "get_stat")
        def wrapper(mock_get_stat, mock_send_discord_message):

            match_data = get_mock_match_data()
            match_timeline = get_mock_match_timeline()

            set_lol_data_context(
                match_data, match_timeline, get_mock_match_data_account_id()
            )
            reset_statistics()

            stat_table = {
                "kills": {"solo_kills": 0, "total_kills": 0, "data": {}},
                "deaths": {
                    "solo_deaths": solo_deaths,
                    "total_deaths": 15,
                    "data": {0: 0, 1: single_champ_solo_deaths},
                    "has_max_deaths": True,
                    "max_deaths_to_champ": {
                        "champ_id": 1,
                        "deaths": single_champ_solo_deaths,
                    },
                },
                "champions": {1: "MasterLi", 0: "AnotherBitch"},
                "winner": {"user": False, "team": 100},
            }

            mock_get_stat.side_effect = lambda x: stat_table[x]

            user = LoLUser(mock_discord_id(), "useless")

            hard_inted = HardIntedRule
            hard_inted.obj.run({}, user)

            func(mock_send_discord_message)

        return wrapper

    return decorator


@should_run()
def test_hard_inted_should_run(response):
    """"""
    assert response


@should_run(solo_deaths=10)
def test_hard_inted_should_run_solo_eq_total(response):
    """"""
    assert response


@should_run(solo_deaths=0, single_champ_solo_deaths=0)
def test_hard_inted_should_run_no_death(response):
    """"""
    assert not response


@should_run(win=True)
def test_hard_inted_should_run_win(response):
    """"""
    assert not response


@run()
def test_hard_inted_run(mock_send_discord_message):
    """"""
    mock_send_discord_message.assert_called_once_with(
        f"well well well, dinner has been served because <@{mock_discord_id()}> fed the absolute shit out of MasterLi giving them 10 / 12 of their solo deaths",
        True,
    )


@run(solo_deaths=10)
def test_hard_inted_run_solo_eq_total(mock_send_discord_message):
    """"""
    mock_send_discord_message.assert_called_once_with(
        f"well well well, dinner has been served because <@{mock_discord_id()}> fed the absolute shit out of MasterLi giving them all 10 of their solo deaths",
        True,
    )
