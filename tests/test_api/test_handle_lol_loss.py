# from tests.mock.mock_match_data import (
#     get_mock_match_data,
#     get_mock_match_data_account_id,
#     get_mock_match_timeline,
# )
# from discord_ritoman.lol.stats.match_stat import (
#     reset_statistics,
#     set_lol_data_context,
# )
# from discord_ritoman.db.schema import LoLText, LoLUser
# import discord_ritoman
# from discord_ritoman.api import handle_lol_loss
# from unittest import mock


# def mock_discord_id() -> int:
#     """
#     The mock discord id used for this testing suite
#     """
#     return 1234


# def handle_lol_loss_helper(
#     solo_deaths: int = 12, single_champ_solo_deaths: int = 10
# ):
#     def decorator(func):
#         @mock.patch.object(discord_ritoman.api, "get_stat")
#         @mock.patch.object(discord_ritoman.api, "send_discord_message")
#         def wrapper(mock_send_discord_message, mock_get_stat):
#             match_data = get_mock_match_data()
#             match_timeline = get_mock_match_timeline()

#             set_lol_data_context(
#                 match_data, match_timeline, get_mock_match_data_account_id()
#             )
#             reset_statistics()

#             stat_table = {
#                 "kills": {"solo_kills": 0, "total_kills": 0, "data": {}},
#                 "deaths": {
#                     "solo_deaths": solo_deaths,
#                     "total_deaths": 15,
#                     "data": {0: 0, 1: single_champ_solo_deaths},
#                     "has_max_deaths": True,
#                 },
#                 "champions": {1: "MasterLi", 0: "AnotherBitch"},
#                 "winner": {"user": False, "team": 100},
#             }

#             mock_get_stat.side_effect = lambda x: stat_table[x]

#             user = LoLUser(mock_discord_id(), "useless")
#             handle_lol_loss(
#                 user,
#                 [LoLText("p", "prefix", 1234)],
#                 [LoLText("sp", "stat_prefix", 1234)],
#                 [LoLText("s", "suffix", 1234)],
#                 "Bitch",
#             )

#             func(mock_send_discord_message)

#         return wrapper

#     return decorator


# @handle_lol_loss_helper()
# def test_handle_lol_loss_hard_inted(mock_send_discord_message):
#     """
#     Tests that the function handle lol loss works correctly
#     when the user being processed has more solo deaths than
#     total_deaths / 2
#     """
#     mock_send_discord_message.assert_called_once_with(
#         f"well well well, dinner has been served because <@{mock_discord_id()}> fed the absolute shit out of MasterLi giving them 10 / 12 of their solo deaths",
#         True,
#     )


# @handle_lol_loss_helper(solo_deaths=10)
# def test_handle_lol_loss_hard_inted_all(mock_send_discord_message):
#     """
#     Tests that the function handle lol loss works correctly
#     when the user being processed has more solo deaths than
#     total_deaths / 2 and all solo deaths go to the same champion
#     """
#     mock_send_discord_message.assert_called_once_with(
#         f"well well well, dinner has been served because <@{mock_discord_id()}> fed the absolute shit out of MasterLi giving them all 10 of their solo deaths",
#         True,
#     )


# @handle_lol_loss_helper(solo_deaths=5, single_champ_solo_deaths=2)
# def test_handle_lol_loss_solo_deaths_gt_solo_kills(mock_send_discord_message):
#     """
#     Tests that the function handle lol loss works correctly
#     when the user being processed has more solo deaths than
#     solo kills
#     """
#     mock_send_discord_message.assert_called_once_with(
#         f"prefix <@{mock_discord_id()}> stat_prefix 5 solo deaths and only 0 solo kills as Bitch in their latest defeat in league of legends. suffix",
#         True,
#     )


# @handle_lol_loss_helper(solo_deaths=0, single_champ_solo_deaths=0)
# def test_handle_lol_loss_solo_deaths_lt_solo_kills(mock_send_discord_message):
#     """
#     Tests that the function handle lol loss works correctly
#     when the user being processed has less solo deaths than
#     solo kills
#     """
#     mock_send_discord_message.assert_called_once_with(
#         f"<@{mock_discord_id()}> got fucking trolled in their last game of league of legends. unlucky m8"
#     )
