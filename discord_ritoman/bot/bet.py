from discord_ritoman.db.accessors import (
    add_lol_user_points,
    create_bet,
    get_lol_user_by_discord_id,
)
from discord_ritoman.db.schema import LoLUser
from typing import Any, Optional
from discord_ritoman.bot.bot_command import bot_command
import time


@bot_command("bet")
class BetCommand:
    @staticmethod
    async def default(ctx: Any, *args: Any, **kwargs: Any):
        """
        Allows a user to place a bet on a player in an active game

        @ritoman casino bet @akash 100 win
        """
        user_id: int = int(args[0][3:-1])
        bet: int = int(args[1])
        prediction: bool = args[2] == "win"

        better_id: int = ctx.message.author.id

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
            return

        if get_lol_user_by_discord_id(user_id) is not None:
            # place bet
            create_bet(
                user_id,
                better_id,
                bet,
                prediction,
                int(time.time() * 1000),  # epoch time in millis
            )
            add_lol_user_points(better_entry, -bet)
            await ctx.send(f"prediction on <@{user_id}> created successfully")
