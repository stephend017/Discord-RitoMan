from discord_ritoman.bot.register import RegisterCommand
from discord_ritoman.db.schema import LoLUser
import pytest

from tests.mock.discord_mocks import mock_discord_user
from tests.helpers import discord_ctx_mock

from unittest import mock

import discord_ritoman.bot.bot
from discord_ritoman.db.session import session


def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    # clean db before insertions
    session.query(LoLUser).delete()
    session.commit()


def teardown_module(module):
    """teardown any state that was previously setup with a setup_module
    method.
    """
    # remove mock users
    session.query(LoLUser).delete()
    session.commit()


@pytest.mark.asyncio
@mock.patch.object(discord_ritoman.bot.register, "get_puuid")
async def test_register(mock_get_puuid):
    """
    Tests that the register command works correctly
    """
    expected_user = mock_discord_user()
    summoner_name = "sevo17"
    discord_user = f"<@!{expected_user.id}>"
    riot_puuid = "APUUID"

    ctx = discord_ctx_mock()
    mock_get_puuid.return_value = riot_puuid

    await RegisterCommand(ctx, discord_user, summoner_name)

    mock_get_puuid.assert_called_once_with(summoner_name)
    ctx.send.assert_called_once_with(
        f"successfully added <@!{expected_user.id}> as the summoner {summoner_name} to the DB"
    )


@pytest.mark.asyncio
async def test_register_get_puuid_fails():
    """
    Tests that the register command fails if the puuid
    does not exist
    """
    expected_user = mock_discord_user()
    summoner_name = "sevo17"
    discord_user = f"<@!{expected_user.id}>"

    ctx = discord_ctx_mock()

    await RegisterCommand(ctx, discord_user, summoner_name)

    ctx.send.assert_called_once_with(
        f"Unable to find summoner {summoner_name}. Are you sure this summoner exists?"
    )
