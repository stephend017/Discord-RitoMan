from discord_ritoman.models import GameResult
import pytest


from typing import List
from discord_ritoman.db.accessors import (
    create_new_lol_user,
    get_all_lol_users,
    get_lol_text_by_group,
    get_lol_user_by_discord_id,
    get_lol_users_with_winrate_enabled,
    reset_all_lol_user_winrate,
    set_lol_user_winrate,
    update_lol_user_last_updated,
    update_lol_user_winrate,
)
from discord_ritoman.db.schema import LoLText, LoLTextGroup, LoLUser
from discord_ritoman.db.session import session


def mock_users() -> List[LoLUser]:
    """
    returns all mock users used by this module
    """
    return [LoLUser(1, "r1"), LoLUser(2, "r2", True), LoLUser(3, "r3", True)]


def mock_text_groups() -> List[LoLTextGroup]:
    """
    Returns all mock text groups used by this module
    """
    return [
        LoLTextGroup("prefix", "text before message", 1234),
        LoLTextGroup("suffix", "text after message", 1234),
    ]


def mock_text(group1: LoLTextGroup, group2: LoLTextGroup) -> List[LoLText]:
    """
    Returns all mock text
    """
    return [
        LoLText("prefix", "testing 1", 1234),
        LoLText("prefix", "2 testing", 1234),
        LoLText("suffix", "another one", 1234),
    ]


def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    # clean db before insertions
    session.query(LoLUser).delete()
    session.commit()

    session.query(LoLText).delete()
    session.commit()

    session.query(LoLTextGroup).delete()
    session.commit()

    # populate db with mock users to test with
    users = mock_users()
    for user in users:
        session.add(user)
        session.commit()

    text_groups = mock_text_groups()
    for text_group in text_groups:
        session.add(text_group)
        session.commit()

    texts = mock_text(text_groups[0], text_groups[1])
    for text in texts:
        session.add(text)
        session.commit()


def teardown_module(module):
    """teardown any state that was previously setup with a setup_module
    method.
    """
    # remove mock users
    session.query(LoLUser).delete()
    session.commit()

    # remove mock text
    session.query(LoLText).delete()
    session.commit()

    # remove mock text_groups
    session.query(LoLTextGroup).delete()
    session.commit()


def test_get_all_lol_users():
    """
    tests that get all lol users works correctly
    """
    expected: List[LoLUser] = mock_users()
    users: List[LoLUser] = get_all_lol_users()
    for user in users:
        found = False
        for e_user in expected:
            if (
                e_user.discord_id == user.discord_id
                and e_user.riot_puuid == user.riot_puuid
                and e_user.winrate == user.winrate
            ):
                found = True
                break
        assert found


def test_get_lol_text_by_group():
    """
    Tests that text can be queried by group
    """
    texts = get_lol_text_by_group("prefix")
    groups = mock_text_groups()
    expected_texts = mock_text(groups[0], groups[1])[:-1]  # only use first 2
    for expected in expected_texts:
        found = False
        for text in texts:
            if expected.content == text.content:
                found = True
                break
        assert found


def test_update_lol_user_last_updated():
    """
    Tests that a user's last update time works correctly
    """
    user = mock_users()[0]
    update_lol_user_last_updated(user, -10)
    assert user.last_updated == -10


def test_update_lol_user_winrate():
    """
    Tests that a user's winrate can be updated sucessfully
    """
    user = mock_users()[1]  # user with winrate enabled
    assert user.wins == 0
    assert user.losses == 0

    update_lol_user_winrate(user, GameResult.WIN)
    user = (
        session.query(LoLUser)
        .filter(LoLUser.discord_id == user.discord_id)
        .one()
    )
    assert user.wins == 1

    update_lol_user_winrate(user, GameResult.LOSS)
    # assert user.losses.compare(LoLUser.losses + 1)
    user = (
        session.query(LoLUser)
        .filter(LoLUser.discord_id == user.discord_id)
        .one()
    )
    assert user.losses == 1

    update_lol_user_winrate(user, GameResult.NONE)
    # assert user.wins.compare(LoLUser.wins + 1) and user.losses.compare(
    #     LoLUser.losses + 1
    # )
    user = (
        session.query(LoLUser)
        .filter(LoLUser.discord_id == user.discord_id)
        .one()
    )
    assert user.wins == 1 and user.losses == 1


def test_set_lol_user_winrate():
    """
    Tests that setting a winrate state (true or false) works correctly
    """
    user = mock_users()[0]
    assert not user.winrate

    set_lol_user_winrate(user, True)
    assert user.winrate

    set_lol_user_winrate(user, False)
    assert not user.winrate


def test_get_lol_users_with_winrate_enabled():
    """
    Tests that getting a users with winrate enabled returns true
    """

    users = get_lol_users_with_winrate_enabled()
    for user in users:
        found = True
        for e_user in mock_users()[1:]:
            if e_user.discord_id == user.discord_id:
                found = True
                break
        assert found


def test_create_new_lol_user():
    """
    Tests that creating a new lol user works correctly
    """
    current = session.query(LoLUser).all()
    assert len(current) == 3
    create_new_lol_user(4, "r4")
    assert len(session.query(LoLUser).all()) == 4


def test_get_lol_user_by_discord_id():
    """
    Tests that getting a user by their given discord id
    works correctly
    """
    assert get_lol_user_by_discord_id(1)
    assert get_lol_user_by_discord_id(6) is None


def test_reset_all_lol_user_winrate():
    """
    Tests that reset all lol user winrate works
    """
    user = mock_users()[2]
    update_lol_user_winrate(user, GameResult.LOSS)
    update_lol_user_winrate(user, GameResult.WIN)

    reset_all_lol_user_winrate()

    assert user.wins == 0
    assert user.losses == 0
