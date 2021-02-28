from typing import List
from discord_ritoman.db.schema import LoLUser
from discord_ritoman.lol.rules.winrate_eod import WinrateEODRule
import discord_ritoman.lol.rules.winrate_eod
from unittest import mock


def should_run_eod():
    def decorator(func):
        def wrapper():
            winrate = WinrateEODRule
            response = winrate.obj.should_run({})
            func(response)

        return wrapper

    return decorator


def run_eod(users: List[LoLUser] = [LoLUser(1, "p1", True, 1, 1)]):
    def decorator(func):
        @mock.patch.object(
            discord_ritoman.lol.rules.winrate_eod,
            "get_lol_users_with_winrate_enabled",
        )
        @mock.patch.object(
            discord_ritoman.lol.rules.winrate_eod, "send_discord_message"
        )
        def wrapper(
            mock_send_discord_message, mock_get_lol_users_with_winrate_enabled
        ):
            mock_get_lol_users_with_winrate_enabled.return_value = users
            winrate = WinrateEODRule
            winrate.obj.run({})
            func(mock_send_discord_message, users)

        return wrapper

    return decorator


@should_run_eod()
def test_should_run(response):
    """"""
    assert response


@run_eod(users=[])
def test_run_no_users(mock_send_discord_message, users):
    """"""
    assert len(users) == 0
    mock_send_discord_message.assert_any_call(
        "Well fuck you little shits didn't play a single game. how sad."
    )


@run_eod()
def test_run_eq(mock_send_discord_message, users):
    """"""
    for user in users:
        mock_send_discord_message.assert_any_call(
            f"<@{user.discord_id}> fucking wasted their time today with {user.wins} wins and {user.losses} losses"
        )


@run_eod(users=[LoLUser(1, "p1", True, 1, 2)])
def test_run_loss_gt_win(mock_send_discord_message, users):
    """"""
    for user in users:
        mock_send_discord_message.assert_any_call(
            f"<@{user.discord_id}> inted today with {user.wins} wins and {user.losses} losses. you fucked up, but im sure it was your team who trolled and not your fault"
        )


@run_eod(users=[LoLUser(1, "p1", True, 2, 1)])
def test_run_loss_lt_win(mock_send_discord_message, users):
    """"""
    for user in users:
        mock_send_discord_message.assert_any_call(
            f"<@{user.discord_id}> carried today with {user.wins} wins and {user.losses} losses, good job summoner"
        )


@run_eod(users=[LoLUser(1, "p1", True)])
def test_run_skip_user(mock_send_discord_message, users):
    """"""
    assert len(users) > 0
    mock_send_discord_message.assert_any_call(
        "Well fuck you little shits didn't play a single game. how sad."
    )
