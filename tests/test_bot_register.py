import pytest

from tests.mock.discord_mocks import mock_discord_bot, mock_discord_user
from tests.helpers import discord_ctx_mock

from unittest import mock

import discord_ritoman.bot
from discord_ritoman.bot import register


@pytest.mark.asyncio
@mock.patch.object(discord_ritoman.bot, "add_new_lol_user")
@mock.patch.object(discord_ritoman.bot, "add_new_discord_user")
@mock.patch.object(discord_ritoman.bot, "get_puuid")
@mock.patch.object(discord_ritoman.bot, "bot")
async def test_register(
    mock_bot, mock_get_puuid, mock_add_new_discord_user, mock_add_new_lol_user
):
    """
    tests that the register function works correctly
    """
    expected_user = mock_discord_user()
    summoner_name = "sevo17"
    discord_user = f"<@!{expected_user.id}>"
    riot_puuid = "APUUID"

    ctx = discord_ctx_mock()
    mock_discord_bot(mock_bot, [expected_user])
    mock_get_puuid.return_value = riot_puuid
    mock_add_new_lol_user.return_value = True

    await register(ctx, discord_user, summoner_name)

    mock_bot.fetch_user.assert_called_once_with(expected_user.id)
    mock_get_puuid.assert_called_once_with(summoner_name)
    mock_add_new_discord_user.assert_called_once_with(
        expected_user.name, riot_puuid, expected_user.id
    )
    mock_add_new_lol_user.assert_called_once_with(expected_user.name)

    ctx.send.assert_called_once_with(
        f"successfully added <@!{expected_user.id}> as the summoner {summoner_name} to the DB"
    )


@pytest.mark.asyncio
@mock.patch.object(discord_ritoman.bot, "bot")
async def test_register_fetch_user_fails(mock_bot):
    """
    Tests that when `fetch_user` fails the correct output
    is sent to the server
    """
    user = mock_discord_user()
    summoner_name = "sevo17"
    discord_user = f"<@!{user.id}>"

    ctx = discord_ctx_mock()
    mock_discord_bot(mock_bot)

    await register(ctx, discord_user, summoner_name)

    ctx.send.assert_called_once_with("Failed to fetch user discord ID")


@pytest.mark.asyncio
@mock.patch.object(discord_ritoman.bot, "bot")
async def test_register_get_puuid_fails(mock_bot):
    """
    Tests that when `get_puuid` fails the correct output
    is sent to the server
    """
    expected_user = mock_discord_user()
    summoner_name = "sevo17"
    discord_user = f"<@!{expected_user.id}>"

    ctx = discord_ctx_mock()
    mock_discord_bot(mock_bot, [expected_user])

    await register(ctx, discord_user, summoner_name)

    mock_bot.fetch_user.assert_called_once_with(expected_user.id)
    ctx.send.assert_called_once_with(
        f"Unable to find summoner {summoner_name}. Are you sure this summoner exists?"
    )


@pytest.mark.asyncio
@mock.patch.object(discord_ritoman.bot, "get_puuid")
@mock.patch.object(discord_ritoman.bot, "bot")
async def test_register_add_new_discord_user_fails(mock_bot, mock_get_puuid):
    """
    Tests that when `add_new_discord_user_fails` fails the correct output
    is sent to the server
    """
    expected_user = mock_discord_user()
    summoner_name = "sevo17"
    discord_user = f"<@!{expected_user.id}>"

    ctx = discord_ctx_mock()
    mock_discord_bot(mock_bot, [expected_user])

    await register(ctx, discord_user, summoner_name)

    mock_bot.fetch_user.assert_called_once_with(expected_user.id)
    mock_get_puuid.assert_called_once_with(summoner_name)

    ctx.send.assert_called_once_with("Failed to update discord_users db")


@pytest.mark.asyncio
@mock.patch.object(discord_ritoman.bot, "add_new_discord_user")
@mock.patch.object(discord_ritoman.bot, "get_puuid")
@mock.patch.object(discord_ritoman.bot, "bot")
async def test_register_add_new_lol_user_fails(
    mock_bot, mock_get_puuid, mock_add_new_discord_user
):
    """
    Tests that when `add_new_lol_user_fails` fails the correct output
    is sent to the server
    """
    expected_user = mock_discord_user()
    summoner_name = "sevo17"
    discord_user = f"<@!{expected_user.id}>"
    riot_puuid = "APUUID"

    ctx = discord_ctx_mock()
    mock_discord_bot(mock_bot, [expected_user])
    mock_get_puuid.return_value = riot_puuid

    await register(ctx, discord_user, summoner_name)

    mock_bot.fetch_user.assert_called_once_with(expected_user.id)
    mock_get_puuid.assert_called_once_with(summoner_name)
    mock_add_new_discord_user.assert_called_once_with(
        expected_user.name, riot_puuid, expected_user.id
    )

    ctx.send.assert_called_once_with("Failed to update lol_data db")
