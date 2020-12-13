import os
import requests

import logging
from logging.handlers import RotatingFileHandler

log_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s"
)

logFile = "./discord_api.log"

my_handler = RotatingFileHandler(
    logFile,
    mode="a",
    maxBytes=5 * 1024 * 1024,
    backupCount=2,
    encoding=None,
    delay=0,
)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)

logger = logging.getLogger("root")
logger.setLevel(logging.INFO)

logger.addHandler(my_handler)


def send_discord_message(message: str):
    """
    Sends a message to the discord server

    To @ a user it must be in the following format
    <@user_id> where user_id is the discord id for
    that user.

    Args:
        message (str): the literal text to send.
    """
    webhook = os.getenv("DISCORD_BOT", None,)
    if webhook is None:
        logger.critical("Unable to read webhook from environment variable")
        return

    response = requests.post(webhook, json={"content": message})

    if not response.ok:
        print(
            f"Failed to send message to discord. Error Code [{response.status_code}]: {response.content}"
        )
