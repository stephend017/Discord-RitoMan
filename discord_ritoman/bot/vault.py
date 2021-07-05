from discord_ritoman.db.accessors import get_all_lol_users
from discord_ritoman.bot.bot_command import bot_command
from typing import Any


@bot_command("vault")
class VaultCommand:
    @staticmethod
    async def default(ctx: Any, *args: Any, **kwargs: Any):
        """
        shows all player points or a specific players points
        """
        players = get_all_lol_users()

        message = "Player totals:\n"
        for user in players:
            message += f"<@{user.discord_id}> {user.points}\n"

        await ctx.send(message)
