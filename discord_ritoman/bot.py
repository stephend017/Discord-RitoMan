from discord_ritoman.lol_api import get_puuid
from discord.ext import commands
import os
import logging
from discord_ritoman.db_api import add_new_discord_user, add_new_lol_user

from discord.user import User

bot = commands.Bot(command_prefix="<@!779328785043554334> ")

logger = logging.Logger("Discord Bot Logger")
logger.addHandler(logging.FileHandler("./bot.log"))


@bot.command()
async def denounce(ctx, user):
    """
    denounces a user
    """
    await ctx.send(f"{user} is tonights biggest loser")


# TODO flame command
# scenario cj talking shit, akshay wants to put him
# in his place. the solution the flame command.
# askhay invokes @ritoman flame @Mars. the bot then
# searches for a statline that is better for akshay
# command will not work if akshay does not play LoL


@bot.command()
async def register(ctx, discord_user, summoner_name):
    """
    Associates a discord user with their LoL account.

    Note: if `summoner_name` is mulitple words it must be surrounded
        by quotes. example "Fwee ba Jee Ba"
    """
    user_id = discord_user[3:-1]
    user: User = None

    try:
        user = await bot.fetch_user(int(user_id))
    except Exception:
        logger.error("Failed to fetch user discord ID")
        await ctx.send("Failed to fetch user discord ID")
        return

    username = user.name
    riot_puuid = ""

    try:
        riot_puuid = get_puuid(summoner_name)
    except Exception:
        logger.error(
            f"Unable to find summoner {summoner_name}. Are you sure this summoner exists?"
        )
        await ctx.send(
            f"Unable to find summoner {summoner_name}. Are you sure this summoner exists?"
        )
        return

    try:
        add_new_discord_user(username, riot_puuid, user_id)
    except Exception:
        logger.critical("Failed to update discord_users db")
        await ctx.send("Failed to update discord_users db")
        return

    try:
        add_new_lol_user(username)
    except Exception:
        logger.critical("Failed to update lol_data db")
        await ctx.send("Failed to update lol_data db")
        return

    await ctx.send(
        f"successfully added <@!{user_id}> as the summoner {summoner_name} to the DB"
    )


def main():
    """
    """
    token: str = os.getenv("DISCORD_RITOMAN_BOT", None)
    if token is None:
        logger.critical("Failed to load Discord bot token.")
        raise Exception("Failed to load Discord bot token.")
    bot.run(token)


if __name__ == "__main__":
    main()
