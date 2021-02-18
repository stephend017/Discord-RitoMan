import os
import requests

from discord_ritoman.utils import create_logger, dynamic_import_class


logger = create_logger(__file__)


def send_discord_message(message: str):
    """
    Sends a message to the discord server

    To @ a user it must be in the following format
    <@user_id> where user_id is the discord id for
    that user.

    Args:
        message (str): the literal text to send.
    """
    webhook = os.getenv("DISCORD_BOT", None)
    if webhook is None:
        logger.critical("Unable to read webhook from environment variable")
        return

    response = requests.post(webhook, json={"content": message})

    if not response.ok:
        print(
            f"Failed to send message to discord. Error Code [{response.status_code}]: {response.content}"
        )
