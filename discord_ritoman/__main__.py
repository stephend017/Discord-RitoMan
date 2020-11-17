import schedule
from discord_ritoman.api import run_lol
import time


def main():
    """
    """
    schedule.every(5).minutes.do(run_lol)

    while True:
        schedule.run_pending()
        time.sleep(60)  # check every minute


if __name__ == "__main__":
    main()
