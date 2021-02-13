from discord_ritoman.db.accessors import get_lol_user_by_discord_id
from discord_ritoman.db.schema import LoLUser
from discord_ritoman.db.session import session
from discord.errors import NotFound
import pytest

from unittest import mock

from tests.mock.discord_mocks import mock_discord_bot, mock_discord_user
from tests.helpers import discord_ctx_mock

import discord_ritoman.bot
from discord_ritoman.bot import winrate


def lol_user_discord_id() -> int:
    """
    returns the discord id of the user
    """
    return 1234


def create_user():
    """
    adds the user to the db
    """
    user = LoLUser(lol_user_discord_id(), "puuid", True)
    session.add(user)
    session.commit()


def remove_all_users():
    """
    removes all the users from the db
    """
    session.query(LoLUser).delete()
    session.commit()


def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    # clean db before insertions
    remove_all_users()
    create_user()


def teardown_module(module):
    """teardown any state that was previously setup with a setup_module
    method.
    """
    remove_all_users()


def winrate_test_helper(
    is_registered=True,
    does_record_winrate=True,
    wins=2,
    losses=2,
    fetch_user_fail=False,
    option="--add",
):
    def decorator(func):
        @pytest.mark.asyncio
        @mock.patch.object(discord_ritoman.bot, "bot")
        async def wrapper(mock_bot):
            ctx = discord_ctx_mock()
            user = None
            discord_user = mock_discord_user(user_id=lol_user_discord_id())

            remove_all_users()

            if is_registered:
                create_user()
                user = get_lol_user_by_discord_id(lol_user_discord_id())
                session.query(LoLUser).filter(
                    LoLUser.discord_id == user.discord_id
                ).update(
                    {
                        "winrate": does_record_winrate,
                        "wins": wins,
                        "losses": losses,
                    }
                )
                user = get_lol_user_by_discord_id(lol_user_discord_id())

            mock_discord_bot(
                mock_bot, [NotFound] if fetch_user_fail else [discord_user]
            )

            discord_id = user.discord_id if user else 0
            # call actual function with everything mocked above
            await winrate(ctx, option, f"<@!{discord_id}>")

            # validate function
            func(ctx, user, discord_user.name)

        return wrapper

    return decorator


@winrate_test_helper(does_record_winrate=False)
def test_winrate_add(ctx, user, username):
    """
    Tests that the winrate --add command works correctly
    """
    ctx.send.assert_called_once_with(f"successfully added {username}")


@winrate_test_helper(option="--get")
def test_winrate_get(ctx, user, username):
    """
    Tests that the winrate --get command works correctly
    """
    ctx.send.assert_called_once_with(
        f"the winrate for <@!{user.discord_id}> today is 2 wins and 2 losses"
    )


@winrate_test_helper(option="--remove")
def test_winrate_remove(ctx, user, username):
    """
    Tests that the winrate --remove command works correctly
    """
    ctx.send.assert_called_once_with(f"successfully removed {username}")


@winrate_test_helper(option="--invalid")
def test_winrate_invalid_option(ctx, user, username):
    """
    Tests that the winrate --remove command works correctly
    """
    ctx.send.assert_called_once_with("<:PepoG:773739956958658560>")


@winrate_test_helper(fetch_user_fail=True)
def test_winrate_fetch_user_fails(ctx, user, username):
    """
    Tests that the winrate command fails when `fetch_user` fails
    """
    ctx.send.assert_called_once_with("<:PepoG:773739956958658560>")


@winrate_test_helper(is_registered=False)
def test_winrate_username_not_registered(ctx, user, username):
    """
    Tests that the winrate command fails when the username
    passed to the command is not registered
    """
    ctx.send.assert_called_once_with("<:PepoG:773739956958658560>")


@winrate_test_helper()
def test_winrate_add_existing_user(ctx, user, username):
    """
    Tests that the winrate command fails when the username
    passed to the command is already added to the winrate table
    """
    ctx.send.assert_called_once_with("<:PepoG:773739956958658560>")
