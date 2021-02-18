from discord_ritoman.bot_.bot_command import bot_command
from discord_ritoman.db.schema import LoLUser
from discord_ritoman.db.accessors import (
    add_lol_text,
    add_lol_text_group,
    create_new_lol_user,
    get_lol_user_by_discord_id,
    set_lol_user_winrate,
)
from discord_ritoman.lol_api import get_puuid
from discord.ext import commands
import os

from discord_ritoman.utils import create_logger


bot = commands.Bot(command_prefix="<@!779328785043554334> ")

logger = create_logger(__file__)


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
    user_id = int(discord_user[3:-1])
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

    create_new_lol_user(user_id, riot_puuid)

    await ctx.send(
        f"successfully added <@!{user_id}> as the summoner {summoner_name} to the DB"
    )


async def winrate_add_helper(ctx, user: LoLUser):
    """
    winrate add helper function (to reduce single function complexity)

    Args:
        ctx: the discord context object sent to the command function
        username: the username of the discord user
    """
    if user.winrate:
        await ctx.send("<:PepoG:773739956958658560>")
        return

    username: str = ""
    try:
        username = (await bot.fetch_user(user.discord_id)).name
    except Exception:
        await ctx.send("<:PepoG:773739956958658560>")
        return

    set_lol_user_winrate(user, True)
    await ctx.send(f"successfully added {username}")


async def winrate_remove_helper(ctx, user: LoLUser):
    """
    winrate helper function (to reduce single function complexity)

    Args:
        ctx: the discord context object sent to the command function
        username: the username of the discord user
    """
    if not user.winrate:
        await ctx.send("<:PepoG:773739956958658560>")
        return

    username: str = ""
    try:
        username = (await bot.fetch_user(user.discord_id)).name
    except Exception:
        await ctx.send("<:PepoG:773739956958658560>")
        return

    set_lol_user_winrate(user, False)

    await ctx.send(f"successfully removed {username}")


async def winrate_get_helper(ctx, user: LoLUser):
    """
    winrate helper function (to reduce single function complexity)

    Args:
        ctx: the discord context object sent to the command function
        username: the username of the discord user
        user_id: the discord id of the discord user
    """
    if not user.winrate:
        await ctx.send("<:PepoG:773739956958658560>")
        return

    await ctx.send(
        f"the winrate for <@!{user.discord_id}> today is {user.wins} wins and {user.losses} losses"
    )


@bot.command()
async def winrate(ctx, option, discord_user):
    """
    The winrate command for the discord ritoman bot

    Args:
        option: What specific subcommand to run (--add, --remove, --get)
        discord_user: should be a server member in the form of @username
    """
    user_id = int(discord_user[3:-1])
    user = get_lol_user_by_discord_id(user_id)

    if user is None:
        await ctx.send("<:PepoG:773739956958658560>")
        return

    if option == "--add":
        return await winrate_add_helper(ctx, user)
    elif option == "--remove":
        return await winrate_remove_helper(ctx, user)
    elif option == "--get":
        return await winrate_get_helper(ctx, user)

    await ctx.send("<:PepoG:773739956958658560>")


@bot.command()
async def textgroup(
    ctx, option: str, group_name: str = "", group_description: str = ""
):
    """
    command to modify a text group
    """
    author_id = ctx.message.author.id

    # TODO check author permissions

    if option == "--list":
        # db table dump
        raise NotImplementedError
    if option == "--add":
        # add to db
        add_lol_text_group(group_name, group_description, author_id)

    if option == "--remove":
        # remove from db
        raise NotImplementedError

    await ctx.send("<:PepoG:773739956958658560>")


@bot.command()
async def text(ctx, option: str, group_name: str = "", content: str = ""):
    """
    command to modify a text
    """
    author_id = ctx.message.author.id

    # TODO check author permissions

    if option == "--list":
        # db table dump
        raise NotImplementedError
    if option == "--add":
        # add to db
        add_lol_text(group_name, content, author_id)

    if option == "--remove":
        # remove from db
        raise NotImplementedError

    await ctx.send("<:PepoG:773739956958658560>")


def main():
    """"""
    token: str = os.getenv("DISCORD_RITOMAN_BOT", None)
    if token is None:
        logger.critical("Failed to load Discord bot token.")
        raise Exception("Failed to load Discord bot token.")
    bot.run(token)


if __name__ == "__main__":
    main()
