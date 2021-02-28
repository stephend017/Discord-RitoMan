from discord_ritoman.models import GameResult
from typing import List
from discord_ritoman.db.schema import LoLUser
import discord_ritoman.lol.rules.winrate_ge
from unittest import mock
from discord_ritoman.lol.rules.winrate_ge import WinrateGERule


def should_run_ge(user: LoLUser = LoLUser(1, "P1", True)):
    """"""

    def decorator(func):
        """"""

        def wrapper():
            winrate = WinrateGERule
            response = winrate.obj.should_run({}, user)

            func(response)

        return wrapper

    return decorator


def run_ge(
    user: LoLUser = LoLUser(1, "P1", True, 1, 1), game_result: bool = True
):
    """"""

    def decorator(func):
        """"""

        @mock.patch.object(discord_ritoman.lol.rules.winrate_ge, "get_stat")
        @mock.patch.object(
            discord_ritoman.lol.rules.winrate_ge, "update_lol_user_winrate"
        )
        def wrapper(mock_update_lol_user_winrate, mock_get_stat):
            stat_table = {"winner": {"user": game_result}}

            mock_get_stat.side_effect = lambda x: stat_table[x]

            winrate = WinrateGERule
            winrate.obj.run({}, user)

            func(mock_update_lol_user_winrate, user)

        return wrapper

    return decorator


@should_run_ge()
def test_should_run(response):
    """"""
    assert response


@should_run_ge(user=LoLUser(1, "P1", False))
def test_should_run_not_enabled(response):
    """"""
    assert not response


@run_ge()
def test_run(mock_update_lol_user_winrate, user):
    """"""
    mock_update_lol_user_winrate.assert_called_once_with(user, GameResult.WIN)


@run_ge(game_result=False)
def test_run_loss(mock_update_lol_user_winrate, user):
    """"""
    mock_update_lol_user_winrate.assert_called_once_with(user, GameResult.LOSS)
