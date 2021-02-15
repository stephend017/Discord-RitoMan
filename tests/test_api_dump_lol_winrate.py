from typing import List
from discord_ritoman.db.schema import LoLUser
from discord_ritoman.api import dump_lol_winrate
from unittest import mock
import discord_ritoman


def dump_lol_winrate_helper(users: List[LoLUser] = [LoLUser(1, "P1", True)]):
    """"""

    def decorator(func):
        """"""

        @mock.patch.object(
            discord_ritoman.api, "get_lol_users_with_winrate_enabled"
        )
        @mock.patch.object(discord_ritoman.api, "send_discord_message")
        def wrapper(
            mock_send_discord_message, mock_get_lol_users_with_winrate_enabled
        ):
            mock_get_lol_users_with_winrate_enabled.return_value = users
            dump_lol_winrate()
            func(mock_send_discord_message)

        return wrapper

    return decorator


@dump_lol_winrate_helper()
def test_dump_lol_winrate_no_users_played(mock_send_discord_message):
    """
    Tests that lol winrate doesn't display a message for a user when no
    games were played by them
    """
    mock_send_discord_message.assert_has_calls(
        [
            mock.call(
                "good evening degens, I'm here to glorify those who carried and shame those who inted"
            ),
            mock.call(
                "Well fuck you little shits didn't play a single game. how sad."
            ),
        ]
    )


@dump_lol_winrate_helper(users=[LoLUser(1, "P1", wins=1, losses=1)])
def test_dump_lol_winrate_equal_wins(mock_send_discord_message):
    """
    Tests that lol winrate doesn't display a message for a user when they
    have equal wins and losses
    """
    mock_send_discord_message.assert_has_calls(
        [
            mock.call(
                "good evening degens, I'm here to glorify those who carried and shame those who inted"
            ),
            mock.call(
                "<@1> fucking wasted their time today with 1 wins and losses"
            ),
        ]
    )


@dump_lol_winrate_helper(users=[LoLUser(1, "P1", wins=2, losses=1)])
def test_dump_lol_winrate_more_wins(mock_send_discord_message):
    """
    Tests that lol winrate doesn't display a message for a user when they
    have more wins than losses
    """
    mock_send_discord_message.assert_has_calls(
        [
            mock.call(
                "good evening degens, I'm here to glorify those who carried and shame those who inted"
            ),
            mock.call(
                "<@1> carried today with 2 wins and 1 losses, good job summoner"
            ),
        ]
    )


@dump_lol_winrate_helper(users=[LoLUser(1, "P1", wins=1, losses=2)])
def test_dump_lol_winrate_more_losses(mock_send_discord_message):
    """
    Tests that lol winrate doesn't display a message for a user when they
    have more losses than wins
    """
    mock_send_discord_message.assert_has_calls(
        [
            mock.call(
                "good evening degens, I'm here to glorify those who carried and shame those who inted"
            ),
            mock.call(
                "<@1> inted today with 1 wins and 2 losses. you fucked up, but im sure it was your team who trolled and not your fault"
            ),
        ]
    )


@dump_lol_winrate_helper(
    users=[LoLUser(1, "P1"), LoLUser(2, "P2", wins=1, losses=2)]
)
def test_dump_lol_winrate_skip_user(mock_send_discord_message):
    """
    Tests that lol winrate doesn't display a message for a user when they
    have more losses than wins
    """
    mock_send_discord_message.assert_has_calls(
        [
            mock.call(
                "good evening degens, I'm here to glorify those who carried and shame those who inted"
            ),
            mock.call(
                "<@2> inted today with 1 wins and 2 losses. you fucked up, but im sure it was your team who trolled and not your fault"
            ),
        ]
    )
