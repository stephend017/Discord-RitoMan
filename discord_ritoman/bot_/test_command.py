# temporary
from discord_ritoman.bot_.bot_command import bot_command


@bot_command("testcommand")
class MyBotCommand:
    @staticmethod
    async def default(ctx, *args, **kwargs):
        await ctx.send("yes")
