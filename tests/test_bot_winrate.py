from discord.errors import NotFound
import pytest

from unittest import mock

from tests.mock.discord_mocks import mock_discord_bot, mock_discord_user
from tests.helpers import discord_ctx_mock

import discord_ritoman.bot
from discord_ritoman.bot import winrate


def winrate_test_helper(
    opt_in=True,
    opt_out=True,
    is_registered=True,
    does_record_winrate=True,
    get_discord_lol_record=[2, 2],
    fetch_user_fail=False,
    option="--add",
):
    def decorator(func):
        @pytest.mark.asyncio
        @mock.patch.object(discord_ritoman.bot, "get_discord_lol_record")
        @mock.patch.object(discord_ritoman.bot, "does_user_record_lol_winrate")
        @mock.patch.object(discord_ritoman.bot, "opt_out_record_lol_winrate")
        @mock.patch.object(discord_ritoman.bot, "opt_in_record_lol_winrate")
        @mock.patch.object(discord_ritoman.bot, "is_user_registered")
        @mock.patch.object(discord_ritoman.bot, "bot")
        async def wrapper(
            mock_bot,
            mock_is_user_registered,
            mock_opt_in_record_lol_winrate,
            mock_opt_out_record_lol_winrate,
            mock_does_user_record_lol_winrate,
            mock_get_discord_lol_record,
        ):
            ctx = discord_ctx_mock()
            user = mock_discord_user()

            mock_is_user_registered.return_value = is_registered
            mock_opt_in_record_lol_winrate.return_value = opt_in
            mock_opt_out_record_lol_winrate.return_value = opt_out
            mock_does_user_record_lol_winrate.return_value = (
                does_record_winrate
            )
            mock_get_discord_lol_record.return_value = get_discord_lol_record

            mock_discord_bot(
                mock_bot, [NotFound] if fetch_user_fail else [user]
            )

            # call actual function with everything mocked above
            await winrate(ctx, option, f"<@!{user.id}>")

            # validate function
            func(ctx, user)

        return wrapper

    return decorator


@winrate_test_helper(does_record_winrate=False)
def test_winrate_add(ctx, user):
    """
    Tests that the winrate --add command works correctly
    """
    ctx.send.assert_called_once_with(f"successfully added {user.name}")


@winrate_test_helper(option="--get")
def test_winrate_get(ctx, user):
    """
    Tests that the winrate --get command works correctly
    """
    ctx.send.assert_called_once_with(
        f"the winrate for <@!{user.id}> today is 2 wins and 2 losses"
    )


@winrate_test_helper(option="--remove")
def test_winrate_remove(ctx, user):
    """
    Tests that the winrate --remove command works correctly
    """
    ctx.send.assert_called_once_with(f"successfully removed {user.name}")


@winrate_test_helper(option="--invalid")
def test_winrate_invalid_option(ctx, user):
    """
    Tests that the winrate --remove command works correctly
    """
    ctx.send.assert_called_once_with("<:PepoG:773739956958658560>")


@winrate_test_helper(fetch_user_fail=True)
def test_winrate_fetch_user_fails(ctx, user):
    """
    Tests that the winrate command fails when `fetch_user` fails
    """
    ctx.send.assert_called_once_with("Failed to fetch user discord ID")


@winrate_test_helper(is_registered=False)
def test_winrate_username_not_registered(ctx, user):
    """
    Tests that the winrate command fails when the username
    passed to the command is not registered
    """
    ctx.send.assert_called_once_with(
        f"{user.name} is not registered, please run the `register` command first"
    )


@winrate_test_helper()
def test_winrate_add_existing_user(ctx, user):
    """
    Tests that the winrate command fails when the username
    passed to the command is already added to the winrate table
    """
    ctx.send.assert_called_once_with("<:PepoG:773739956958658560>")


@winrate_test_helper(does_record_winrate=False, opt_in=False)
def test_winrate_add_opt_in_fails(ctx, user):
    """
    Tests that the winrate command fails when the opt in
    db query fails
    """
    ctx.send.assert_called_once_with(
        "<@!383854815186518016> `opt_in_record_lol_winrate` failed and its probably your fault."
    )


@winrate_test_helper(option="--remove", opt_out=False)
def test_winrate_remove_opt_out_fails(ctx, user):
    """
    Tests that the winrate command fails when the opt out
    db query fails
    """
    ctx.send.assert_called_once_with(
        "Unfortunately we can't remove you from this service at this time. A report has been filed and your ticker number is `undefined`. Thank you for your patience as we solve this problem."
    )


@winrate_test_helper(get_discord_lol_record=[], option="--get")
def test_winrate_get_lol_record_fails(ctx, user):
    """
    Tests that when get_lol_record fails the correct output is produced
    """
    ctx.send.assert_called_once_with(f"Failed to get winrate for {user.name}")
