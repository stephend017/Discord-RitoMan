# temporary
from discord_ritoman.bot_.bot_command import bot_command


@bot_command("testcommand")
class AnotherBotCommand:
    @staticmethod
    async def default(ctx, *args, **kwargs):
        await ctx.send("yes")
