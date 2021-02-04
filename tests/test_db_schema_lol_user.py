import pytest

from discord_ritoman.db.schema import LoLUser, LoLUserWinrate
from discord_ritoman.db.session import session


@pytest.fixture
def discord_id() -> int:
    return 12345


@pytest.fixture
def riot_puuid() -> str:
    return "testing"


def test_create_lol_user(discord_id, riot_puuid):
    """
    Tests that creating a new LoLUser works correctly
    """
    assert len(session.query(LoLUser).all()) == 0

    user = LoLUser(discord_id, riot_puuid)
    session.add(user)
    session.commit()

    queried_users = session.query(LoLUser).all()

    assert len(queried_users) == 1

    queried_user = queried_users[0]
    assert queried_user.discord_id == discord_id
    assert queried_user.riot_puuid == riot_puuid
    assert queried_user.last_updated > 0


def test_update_lol_user(discord_id, riot_puuid):
    """
    Tests that a LoLUser can be updated
    """
    # check if the user still exists
    queried_users = session.query(LoLUser).all()
    user = None
    if len(queried_users) != 1:
        # user is not present, insert new user
        user = LoLUser(discord_id, riot_puuid)
        session.add(user)
        session.commit()
    else:
        user = queried_users[0]

    user.last_updated = -10
    session.commit()

    assert session.query(LoLUser).all()[0].last_updated == -10


def test_add_lol_user_winrate(discord_id):
    """
    Tests that a LoLUser can have a winrate associated with them
    """
    assert len(session.query(LoLUserWinrate).all()) == 0

    queried_users = session.query(LoLUser).all()
    user = None
    if len(queried_users) != 1:
        # user is not present, insert new user
        user = LoLUser(discord_id, riot_puuid)
        session.add(user)
        session.commit()
    else:
        user = queried_users[0]

    assert user.winrate is None
    winrate = LoLUserWinrate(discord_id)
    user.winrate = discord_id
    session.add(winrate)
    session.commit()

    assert len(session.query(LoLUserWinrate).all()) == 1


def test_delete_lol_user_winrate(discord_id):
    """
    Tests that a LoLUser that has a winrate associated with them
    can be removed
    """
    assert len(session.query(LoLUserWinrate).all()) == 1

    queried_users = session.query(LoLUser).all()
    user = None
    if len(queried_users) != 1:
        # user is not present, insert new user
        user = LoLUser(discord_id, riot_puuid)
        winrate = LoLUserWinrate(discord_id)
        session.add(winrate)
        user.winrate = discord_id
        session.add(user)
        session.commit()
    else:
        user = queried_users[0]

    assert user.winrate == discord_id
    user.winrate = None
    session.query(LoLUserWinrate).filter(
        LoLUserWinrate.discord_id == discord_id
    ).delete()
    session.commit()

    assert len(session.query(LoLUserWinrate).all()) == 0


def test_delete_lol_user(discord_id, riot_puuid):
    """
    Tests that a LoLUser can be deleted
    """
    queried_users = session.query(LoLUser).all()
    user = None
    if len(queried_users) != 1:
        # user is not present, insert new user
        user = LoLUser(discord_id, riot_puuid)
        session.add(user)
        session.commit()
    else:
        user = queried_users[0]

    session.query(LoLUser).filter(LoLUser.discord_id == discord_id).delete()
    session.commit()

    assert len(session.query(LoLUser).all()) == 0
