# temporary
from discord_ritoman.bot.bot_command import bot_command


@bot_command("testcommand")
class AnotherBotCommand:
    @staticmethod
    async def default(ctx, *args, **kwargs):
        await ctx.send("yes")

    @staticmethod
    def help() -> str:
        return "this is a testing command"
