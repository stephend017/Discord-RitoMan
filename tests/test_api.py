from discord_ritoman.db.schema import LoLText, LoLUser
import discord_ritoman
from discord_ritoman.api import handle_lol_loss
from unittest.mock import MagicMock
from unittest import mock
import discord_ritoman.lol_match_data


def mock_discord_id() -> int:
    """
    The mock discord id used for this testing suite
    """
    return 1234


def mock_lol_match_data(
    solo_kills: int = 0,
    solo_killed: int = 12,
    single_champ_solo_kills: int = 0,
    single_champ_solo_deaths: int = 10,
    total_deaths: int = 15,
    has_max_team_deaths: bool = True,
    champ_name: str = "MasterLi",
):
    """
    Returns a mock lol match data object

    Args:
        solo_kills (int): the number of solo kills this user got
        solo_killed (int): the number of solo deaths this user got
        single_champ_solo_kills (int): the number of solo kills on the same champ
            for testing purposes it is assumed this is a max
        single_champ_solo_deaths (int): the number of solor deaths on the same champ
            for testing purposes it is assumed this is a max
        total_deaths (int): the total deaths for this user (solo included)
        has_max_team_deaths (bool): flag if this user died the most on their team
        champ_name (str): value to return from `get_champion_name_from_participant_id`
    """
    mock_lol_match_data = MagicMock()
    mock_lol_match_data.get_solo_kills = MagicMock()
    mock_lol_match_data.get_solo_kills.return_value = solo_kills
    mock_lol_match_data.get_solo_killed = MagicMock()
    mock_lol_match_data.get_solo_killed.return_value = solo_killed
    mock_lol_match_data.get_feeding_data = MagicMock()
    mock_lol_match_data.get_feeding_data.return_value = (
        {3: single_champ_solo_kills},  # who fed me
        {3: single_champ_solo_deaths},  # who i fed
    )
    mock_lol_match_data.get_total_deaths = MagicMock()
    mock_lol_match_data.get_total_deaths.return_value = total_deaths
    mock_lol_match_data.has_max_team_deaths = MagicMock()
    mock_lol_match_data.has_max_team_deaths.return_value = has_max_team_deaths
    mock_lol_match_data.get_champion_name_from_pariticpant_id = MagicMock()
    mock_lol_match_data.get_champion_name_from_pariticpant_id.return_value = (
        champ_name
    )
    return mock_lol_match_data


def handle_lol_loss_helper(
    solo_killed: int = 12, single_champ_solo_deaths: int = 10
):
    def decorator(func):
        @mock.patch.object(discord_ritoman.api, "send_discord_message")
        def wrapper(mock_send_discord_message):
            lol_match_data = mock_lol_match_data(
                solo_killed=solo_killed,
                single_champ_solo_deaths=single_champ_solo_deaths,
            )
            user = LoLUser(mock_discord_id(), "useless")
            handle_lol_loss(
                lol_match_data,
                user,
                [LoLText("p", "prefix", 1234)],
                [LoLText("sp", "stat_prefix", 1234)],
                [LoLText("s", "suffix", 1234)],
                "Bitch",
            )

            func(mock_send_discord_message)

        return wrapper

    return decorator


@handle_lol_loss_helper()
def test_handle_lol_loss_hard_inted(mock_send_discord_message):
    """
    Tests that the function handle lol loss works correctly
    when the user being processed has more solo deaths than
    total_deaths / 2
    """
    mock_send_discord_message.assert_called_once_with(
        f"well well well, dinner has been served because <@{mock_discord_id()}> fed the absolute shit out of MasterLi giving them 10 / 12 of their solo deaths"
    )


@handle_lol_loss_helper(solo_killed=10)
def test_handle_lol_loss_hard_inted_all(mock_send_discord_message):
    """
    Tests that the function handle lol loss works correctly
    when the user being processed has more solo deaths than
    total_deaths / 2 and all solo deaths go to the same champion
    """
    mock_send_discord_message.assert_called_once_with(
        f"well well well, dinner has been served because <@{mock_discord_id()}> fed the absolute shit out of MasterLi giving them all 10 of their solo deaths"
    )


@handle_lol_loss_helper(solo_killed=5, single_champ_solo_deaths=2)
def test_handle_lol_loss_solo_deaths_gt_solo_kills(mock_send_discord_message):
    """
    Tests that the function handle lol loss works correctly
    when the user being processed has more solo deaths than
    solo kills
    """
    mock_send_discord_message.assert_called_once_with(
        f"prefix <@{mock_discord_id()}> stat_prefix 5 solo deaths and only 0 solo kills as Bitch in their latest defeat in league of legends. suffix"
    )


@handle_lol_loss_helper(solo_killed=0, single_champ_solo_deaths=0)
def test_handle_lol_loss_solo_deaths_lt_solo_kills(mock_send_discord_message):
    """
    Tests that the function handle lol loss works correctly
    when the user being processed has less solo deaths than
    solo kills
    """
    mock_send_discord_message.assert_called_once_with(
        f"<@{mock_discord_id()}> got fucking trolled in their last game of league of legends. unlucky m8"
    )
