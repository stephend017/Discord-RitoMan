import os
from discord_ritoman.bot.bot import bot
from discord_ritoman.utils import create_logger

logger = create_logger(__file__)


def main():
    """"""
    token: str = os.getenv("DISCORD_RITOMAN_BOT", None)
    if token is None:
        logger.critical("Failed to load Discord bot token.")
        raise Exception("Failed to load Discord bot token.")

    logger.info(bot.all_commands)
    bot.run(token)


if __name__ == "__main__":
    main()
