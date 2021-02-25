from discord_ritoman.db.schema import LoLUser
from typing import Union
from discord_ritoman.bot import bot
from discord_ritoman.bot.bot_command import bot_command
from discord_ritoman.db.accessors import (
    get_lol_user_by_discord_id,
    set_lol_user_winrate,
)


async def get_user(ctx, discord_user) -> Union[LoLUser, None]:
    """"""
    user_id = int(discord_user[3:-1])
    user = get_lol_user_by_discord_id(user_id)

    if user is None:
        await ctx.send("<:PepoG:773739956958658560>")
        return None

    return user


async def get_username(ctx, user) -> Union[str, None]:
    """"""
    username: str = ""
    try:
        username = (await bot.fetch_user(user.discord_id)).name
    except Exception:
        await ctx.send("<:PepoG:773739956958658560>")
        return None
    return username


async def toggle_winrate(ctx, action, arg0):
    """"""
    user = await get_user(ctx, arg0)
    if user is None:
        return

    if (user.winrate and action == "add") or (
        not user.winrate and action != "add"
    ):
        await ctx.send("<:PepoG:773739956958658560>")
        return

    username = await get_username(ctx, user)
    if username is None:
        return

    set_lol_user_winrate(user, True if action == "add" else False)
    await ctx.send(
        f"successfully {'added' if action == 'add' else 'removed'} {username}"
    )


@bot_command("winrate")
class WinrateCommand:
    @staticmethod
    async def default(ctx, *args, **kwargs):
        """"""
        await ctx.send("<:PepoG:773739956958658560>")

    @staticmethod
    async def option_add(ctx, *args, **kwargs):
        """"""
        await toggle_winrate(ctx, "add", args[0])

    @staticmethod
    async def option_remove(ctx, *args, **kwargs):
        """"""
        await toggle_winrate(ctx, "remove", args[0])

    @staticmethod
    async def option_get(ctx, *args, **kwargs):
        """"""
        user = await get_user(ctx, args[0])
        if user is None:
            return

        if not user.winrate:
            await ctx.send("<:PepoG:773739956958658560>")
            return

        await ctx.send(
            f"the winrate for <@!{user.discord_id}> today is {user.wins} wins and {user.losses} losses"
        )
