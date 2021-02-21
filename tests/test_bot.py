import pytest
import discord
import discord_ritoman.bot.__main__
from discord_ritoman.bot.__main__ import main
from unittest import mock


@pytest.mark.asyncio
@mock.patch.object(discord_ritoman.bot.__main__, "os")
@mock.patch.object(discord_ritoman.bot.__main__, "logger")
def test_bot(mock_logger, mock_os):
    """"""
    mock_os.getenv.return_value = "useless"
    with pytest.raises(discord.errors.LoginFailure):
        main()
    all_commands = mock_logger.info.call_args[0][0]
    assert "denounce" in all_commands
    assert "testcommand" in all_commands
    assert "winrate" in all_commands
