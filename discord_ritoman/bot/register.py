from discord_ritoman.bot.bot_command import bot_command
from discord_ritoman.utils import create_logger
from discord_ritoman.db.accessors import create_new_lol_user
from discord_ritoman.lol_api import get_puuid

logger = create_logger(__file__)


@bot_command("register")
class RegisterCommand:
    @staticmethod
    async def default(ctx, *args, **kwargs):
        user_id: int = int(args[0][3:-1])
        riot_puuid: str = ""
        summoner_name: str = args[1]

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

    @staticmethod
    def help():
        return """
        Associates a discord user with their LoL account.

        Note: if `summoner_name` is mulitple words it must be surrounded
        by quotes. example "Fwee ba Jee Ba"

        Usage:
            @ritoman register <discord_username> <summoner_name>
        """
