from discord.errors import NotFound
import pytest

from unittest import mock
from unittest.mock import AsyncMock, MagicMock
from discord.user import User

import discord_ritoman.bot
from discord_ritoman.bot import register


def discord_ctx_mock() -> MagicMock:
    """
    Returns the ctx object passed to each bot command funciton

    Returns:
        MagicMock: A magic mock that mocks the context object
    """
    ctx = MagicMock()
    ctx.send = AsyncMock()
    return ctx


def discord_bot_mock(mock_bot, fetch_user_result=[NotFound]):
    """
    Adds relevant fields to make the mock passed in
    behave as a bot

    Args:
        mock_bot: the mock to configure
        fetch_user_result: the response to return from the
            fetch user function
    """
    mock_bot.fetch_user = AsyncMock()
    mock_bot.fetch_user.side_effect = fetch_user_result


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
    user_id = 383854815186518016
    expected_user = User(
        state=None,
        data={
            "username": "sevo",
            "discriminator": 4375,
            "avatar": "",
            "id": user_id,
        },
    )
    summoner_name = "sevo17"
    discord_user = f"<@!{user_id}>"
    riot_puuid = "APUUID"

    ctx = discord_ctx_mock()
    discord_bot_mock(mock_bot, [expected_user])
    mock_get_puuid.return_value = riot_puuid
    mock_add_new_lol_user.return_value = True

    await register(ctx, discord_user, summoner_name)

    mock_bot.fetch_user.assert_called_once_with(user_id)
    mock_get_puuid.assert_called_once_with(summoner_name)
    mock_add_new_discord_user.assert_called_once_with(
        expected_user.name, riot_puuid, user_id
    )
    mock_add_new_lol_user.assert_called_once_with(expected_user.name)

    ctx.send.assert_called_once_with(
        f"successfully added <@!{user_id}> as the summoner {summoner_name} to the DB"
    )


@pytest.mark.asyncio
@mock.patch.object(discord_ritoman.bot, "bot")
async def test_register_fetch_user_fails(mock_bot):
    """
    Tests that when `fetch_user` fails the correct output
    is sent to the server
    """
    user_id = 383854815186518016
    summoner_name = "sevo17"
    discord_user = f"<@!{user_id}>"

    ctx = discord_ctx_mock()

    discord_bot_mock(mock_bot)

    await register(ctx, discord_user, summoner_name)

    ctx.send.assert_called_once_with("Failed to fetch user discord ID")


@pytest.mark.asyncio
@mock.patch.object(discord_ritoman.bot, "bot")
async def test_register_get_puuid_fails(mock_bot):
    """
    Tests that when `get_puuid` fails the correct output
    is sent to the server
    """
    user_id = 383854815186518016
    summoner_name = "sevo17"
    discord_user = f"<@!{user_id}>"
    expected_user = User(
        state=None,
        data={
            "username": "sevo",
            "discriminator": 4375,
            "avatar": "",
            "id": user_id,
        },
    )

    ctx = discord_ctx_mock()

    discord_bot_mock(mock_bot, [expected_user])

    await register(ctx, discord_user, summoner_name)

    mock_bot.fetch_user.assert_called_once_with(user_id)
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
    user_id = 383854815186518016
    summoner_name = "sevo17"
    discord_user = f"<@!{user_id}>"
    expected_user = User(
        state=None,
        data={
            "username": "sevo",
            "discriminator": 4375,
            "avatar": "",
            "id": user_id,
        },
    )

    ctx = discord_ctx_mock()

    discord_bot_mock(mock_bot, [expected_user])

    await register(ctx, discord_user, summoner_name)

    mock_bot.fetch_user.assert_called_once_with(user_id)
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
    user_id = 383854815186518016
    summoner_name = "sevo17"
    discord_user = f"<@!{user_id}>"
    expected_user = User(
        state=None,
        data={
            "username": "sevo",
            "discriminator": 4375,
            "avatar": "",
            "id": user_id,
        },
    )
    riot_puuid = "APUUID"

    ctx = discord_ctx_mock()
    discord_bot_mock(mock_bot, [expected_user])
    mock_get_puuid.return_value = riot_puuid

    await register(ctx, discord_user, summoner_name)

    mock_bot.fetch_user.assert_called_once_with(user_id)
    mock_get_puuid.assert_called_once_with(summoner_name)
    mock_add_new_discord_user.assert_called_once_with(
        expected_user.name, riot_puuid, user_id
    )

    ctx.send.assert_called_once_with("Failed to update lol_data db")
