from discord_ritoman.discord_api import send_discord_message
from unittest import mock


@mock.patch("os.getenv")
@mock.patch("requests.post")
def test_send_discord_message(mock_post, mock_getenv):
    """
    Tests that sending a discord message works as expected
    """
    message = "thisisatestingmessage"
    webhook = "thisisadiscordwebhook"

    mock_getenv.return_value = webhook

    mock_post.return_value.ok = True
    mock_post.return_value.status_code = 200
    mock_post.return_value.content = "success"

    send_discord_message(message)

    mock_post.assert_called_once_with(webhook, json={"content": message})
