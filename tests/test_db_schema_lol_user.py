import pytest

from discord_ritoman.db.schema import LoLUser
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
    queried_users = session.query(LoLUser).all()
    if len(queried_users) > 0:
        session.query(LoLUser).delete()
        session.commit()

    assert len(session.query(LoLUser).all()) == 0

    user = LoLUser(discord_id, riot_puuid, winrate=True)
    session.add(user)
    session.commit()

    queried_users = session.query(LoLUser).all()

    assert len(queried_users) == 1

    queried_user = queried_users[0]
    assert queried_user.discord_id == discord_id
    assert queried_user.riot_puuid == riot_puuid
    assert queried_user.last_updated > 0
    assert queried_user.winrate
    assert queried_user.wins == 0
    assert queried_user.losses == 0


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
