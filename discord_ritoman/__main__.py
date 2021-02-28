import schedule
from discord_ritoman.api import poll_lol_api, run_end_of_day
import time


def main():
    """"""
    schedule.every(5).minutes.do(poll_lol_api)

    schedule.every().days.at("12:00:00").do(run_end_of_day)

    # run initially
    poll_lol_api()

    while True:
        schedule.run_pending()
        time.sleep(60)  # check every minute


if __name__ == "__main__":
    main()
