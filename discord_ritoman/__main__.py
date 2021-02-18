from discord_ritoman.bot_.bot_command import bot_command
import schedule
from discord_ritoman.api import dump_lol_winrate, run_lol
import time


def main():
    """"""
    schedule.every(5).minutes.do(run_lol)

    schedule.every().days.at("00:00:00").do(dump_lol_winrate)

    # run initially
    run_lol()

    while True:
        schedule.run_pending()
        time.sleep(60)  # check every minute


# temporary
@bot_command("testcommand")
class MyBotCommand:
    @staticmethod
    async def default(ctx, *args, **kwargs):
        await ctx.send("yes")


if __name__ == "__main__":
    main()
