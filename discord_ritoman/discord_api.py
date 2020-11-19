import os
import requests

import logging

logger = logging.Logger("Discord API Logger")
logger.addHandler(logging.FileHandler("./discord_api.log"))


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
