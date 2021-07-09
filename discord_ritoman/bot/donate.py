from discord_ritoman.db.accessors import (
    add_lol_user_points,
    get_lol_user_by_discord_id,
)
from discord_ritoman.bot.bot_command import bot_command
from typing import Any


@bot_command("donate")
class DonateCommand:
    @staticmethod
    async def default(ctx: Any, *args: Any, **kwargs: Any):
        """
        idk why but donations ig
        """
        poor_person = int(args[0][3:-1])
        amount = int(args[1])

        user = get_lol_user_by_discord_id(ctx.message.author.id)
        poor_person_user = get_lol_user_by_discord_id(poor_person)

        if user is None:
            await ctx.send("idk man you don't exist")
            return

        if poor_person_user is None:
            await ctx.send("unable to find poor people")
            return

        if user.points < amount:
            await ctx.send("you're poor too")
            return

        add_lol_user_points(poor_person_user, amount)
        add_lol_user_points(user, -amount)

        await ctx.send(
            f"<@{user.discord_id}> donated {amount} to <@{poor_person}>"
        )
