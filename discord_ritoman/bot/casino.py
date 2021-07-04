from discord_ritoman.db.schema import LoLUser
from typing import Any, Optional
from discord import User

from discord.ext.commands.context import Context
from discord_ritoman.db.accessors import (
    create_bet,
    get_all_active_bets,
    get_all_active_games,
    get_all_lol_users,
    get_lol_user_by_discord_id,
)
from discord_ritoman.bot.bot_command import bot_command


@bot_command("casino")
class CasinoCommand:
    @staticmethod
    async def default(ctx: Any, *args: Any, **kwargs: Any):
        """
        shows all active bets and all active games
        """
        active_games = get_all_active_games()
        active_bets = get_all_active_bets()

        message = "Welcome to the Casino\n\nActive bets:\n"

        for bet in active_bets:
            message += (
                f"<@{bet.better}> bet {bet.amount} points on <@{bet.player}>\n"
            )

        message += "\nActive games:\n"

        for game in active_games:
            message += (
                f"<@{game.player}> is playing in game_id {game.game_id}\n"
            )

        await ctx.send(message)

    @staticmethod
    async def vault(ctx: Any, *args: Any, **kwargs: Any):
        """
        shows all player points or a specific players points
        """
        players = get_all_lol_users()

        message = "Player totals:\n"
        for user in players:
            message += f"<@{user.discord_id}> {user.points}\n"

        await ctx.send(message)

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
                # place bet
                create_bet(
                    user_id,
                    better_id,
                    better_points,
                    prediction,
                    active_game.game_id,
                )
                await ctx.send("Successfully created bet")

    @staticmethod
    def help():
        # TODO
        return """
        Associates a discord user with their LoL account.

        Note: if `summoner_name` is mulitple words it must be surrounded
        by quotes. example "Fwee ba Jee Ba"

        Usage:
            @ritoman register <discord_username> <summoner_name>
        """
