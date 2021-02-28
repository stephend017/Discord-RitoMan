# from discord_ritoman.api import run_lol
# from discord_ritoman.lol_match_metadata import LoLMatchMetadata
# from typing import Dict, List
# from discord_ritoman.db.schema import LoLText, LoLUser
# from unittest import mock
# import discord_ritoman


# def run_lol_helper(
#     users: List[LoLUser] = [LoLUser(1, "P1")],
#     p0: List[LoLText] = [LoLText("p0", "prefix", 1234)],
#     sp0: List[LoLText] = [LoLText("sp0", "stat_prefix", 1234)],
#     s0: List[LoLText] = [LoLText("s0", "suffix", 1234)],
#     account_ids: Dict[str, str] = {"P1": "A1"},
#     matches: Dict[str, List[LoLMatchMetadata]] = {"A1": [mock.MagicMock()]},
# ):
#     def decorator(func):
#         @mock.patch.object(discord_ritoman.api, "handle_lol_match")
#         @mock.patch.object(discord_ritoman.api, "get_matches")
#         @mock.patch.object(discord_ritoman.api, "get_account_id")
#         @mock.patch.object(discord_ritoman.api, "get_lol_text_by_group")
#         @mock.patch.object(discord_ritoman.api, "get_all_lol_users")
#         def wrapper(
#             mock_get_all_lol_users,
#             mock_get_lol_text_by_group,
#             mock_get_account_id,
#             mock_get_matches,
#             mock_handle_lol_match,
#         ):
#             mock_get_all_lol_users.return_value = users
#             mock_get_lol_text_by_group.side_effect = (
#                 lambda x: p0 if x == "p0" else sp0 if x == "sp0" else s0
#             )
#             mock_get_account_id.side_effect = lambda x: account_ids[x]
#             mock_get_matches.side_effect = lambda x, y: matches[x]

#             run_lol()

#             func(mock_get_account_id, mock_get_matches, mock_handle_lol_match)

#         return wrapper

#     return decorator


# @run_lol_helper()
# def test_run_lol(mock_get_account_id, mock_get_matches, mock_handle_lol_match):
#     """
#     Tests that run lol works correctlys
#     """
#     mock_get_account_id.assert_called_once_with("P1")
#     mock_get_matches.assert_called_once()
#     mock_handle_lol_match.assert_called_once()


# @run_lol_helper(account_ids={})
# def test_run_lol_get_account_id_failed(
#     mock_get_account_id, mock_get_matches, mock_handle_lol_match
# ):
#     """
#     Tests that run lol works correctly when get_accound id fails
#     """
#     mock_get_account_id.assert_called_once_with("P1")
#     mock_get_matches.assert_not_called()
#     mock_handle_lol_match.assert_not_called()


# @run_lol_helper(matches={})
# def test_run_lol_get_matches_failed(
#     mock_get_account_id, mock_get_matches, mock_handle_lol_match
# ):
#     """
#     Tests that run lol works correctly when matches fails
#     """
#     mock_get_account_id.assert_called_once_with("P1")
#     mock_get_matches.assert_called_once()
#     mock_handle_lol_match.assert_not_called()
