import pytest
from unittest.mock import AsyncMock, MagicMock, call
from discord_ritoman.bot import bot
from discord_ritoman.bot_.bot_command import GLOBAL_COMMAND_TABLE, bot_command
from discord_ritoman.utils import create_logger

logger = create_logger(__file__)


@pytest.mark.asyncio
async def test_bot_command_decorator():
    """
    tests that the bot command decorator works correctly
    """
    mock_logger = MagicMock()

    @bot_command("mycommand")
    class MyBotCommand:
        @staticmethod
        async def default(ctx, *args, **kwargs):
            mock_logger("default")
            await ctx.send("yes")

        @staticmethod
        async def option_one(ctx, *args, **kwargs):
            mock_logger("option one")

    count = 0
    for command in bot.commands:
        if command.name in GLOBAL_COMMAND_TABLE:
            count += 1

    assert count == len(GLOBAL_COMMAND_TABLE.items()) > 0
    assert "testcommand" in GLOBAL_COMMAND_TABLE
    assert "mycommand" in GLOBAL_COMMAND_TABLE
    assert "testcommand" in bot.all_commands
    assert "mycommand" in bot.all_commands
    assert "denounce" in bot.all_commands

    await MyBotCommand(AsyncMock(), "one", "four", 3)
    await MyBotCommand(AsyncMock())

    mock_logger.assert_has_calls(
        [call("default"), call("option one")], any_order=True
    )
