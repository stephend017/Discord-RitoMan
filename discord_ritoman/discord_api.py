import os
import requests


def send_discord_message(message: str):
    """
    sends a message to the discord server
    """
    webhook = os.getenv("DISCORD_BOT", None,)
    if webhook is None:
        print("Unable to read webhook from environment variable")
        return

    response = requests.post(webhook, json={"content": message})

    if not response.ok:
        print(
            f"Failed to send message to discord. Error Code [{response.status_code}]: {response.content}"
        )
