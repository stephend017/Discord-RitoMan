from typing import Any
from discord_ritoman.db.accessors import (
    get_all_active_bets,
    get_all_active_games,
)
from discord_ritoman.bot.bot_command import bot_command
import datetime


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
            message += f"<@{bet.better}> bet {bet.amount} points on <@{bet.player}> {'winning' if bet.prediction else 'losing'} their next game at {datetime.datetime.fromtimestamp(bet.created / 1000.0).strftime('%m/%d/%Y, %H:%M:%S')}\n"

        message += "\nActive games:\n"

        for game in active_games:
            message += f"<@{game.player}> is playing in game_id {game.game_id} which started at {datetime.datetime.fromtimestamp(game.start_time / 1000.0).strftime('%m/%d/%Y, %H:%M:%S')}\n"

        await ctx.send(message)

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
