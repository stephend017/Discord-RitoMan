from discord_ritoman.db.accessors import (
    create_bet,
    get_all_active_games,
    get_lol_user_by_discord_id,
)
from discord_ritoman.db.schema import LoLUser
from typing import Any, Optional
from discord.ext.commands.context import Context
from discord import User
from discord_ritoman.bot.bot_command import bot_command
import time


@bot_command("bet")
class BetCommand:
    @staticmethod
    async def bet(ctx: Context, *args: Any, **kwargs: Any):
        """
        Allows a user to place a bet on a player in an active game

        @ritoman casino bet @akash 100 win
        """
        user_id: int = int(args[0][3:-1])
        bet: int = int(args[1])
        prediction: bool = args[2] == "win"

        better: User = ctx.author()[0]
        better_id: int = better.id

        better_entry: Optional[LoLUser] = get_lol_user_by_discord_id(better_id)
        if better_entry is None:
            await ctx.send(
                "Better does not exist in the db. You must be registered to bet"
            )
            return

        better_points: int = better_entry.points
        if better_points < bet:
            await ctx.send(
                f"Unable to create bet. Better only has {better_points}"
            )

        active_games = get_all_active_games()

        for active_game in active_games:
            if user_id == active_game.player:

                if active_game.start_time + 400000 > round(time.time() * 1000):
                    await ctx.send("unable to bet. game has already started")

                # place bet
                create_bet(
                    user_id,
                    better_id,
                    better_points,
                    prediction,
                    active_game.game_id,
                )
                await ctx.send(
                    f"Successfully predicted {'win' if prediction else 'loss'} on <@{user_id}>"
                )
