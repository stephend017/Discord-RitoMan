from discord.errors import NotFound
from discord.user import User
from unittest.mock import AsyncMock


def mock_discord_user(
    username: str = "sevo",
    discriminator: int = 4375,
    user_id: int = 383854815186518016,
) -> User:
    """
    Returns a mock `User` object to test with

    Args:
        username (str): the discord username (name shown on discord profile)
        discriminator (int): the number after the `#` in discord profile name
        user_id (int): the numeric id for each discord user (can be found via
            developer controls `copy id`)

    Returns:
        User: the user object defined by the discord API. NOTE: this object
            is incomplete and does not support all features
    """
    return User(
        state=None,
        data={
            "username": username,
            "discriminator": discriminator,
            "avatar": "",  # currently not needed for testing
            "id": user_id,
        },
    )


def mock_discord_bot(mock_bot, fetch_user_result=[NotFound]):
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


def mock_discord_id() -> int:
    """
    Returns a mock discord id for testing
    """
    return 383854815186518016
