"""
This class is where all database accessor functions will be defined
"""
from typing import List

from sqlalchemy.orm.exc import NoResultFound

from discord_ritoman.models import GameResult
from discord_ritoman.db.schema import LoLText, LoLTextGroup, LoLUser
from discord_ritoman.db.session import session


def get_all_lol_users() -> List[LoLUser]:
    """
    Returns a list of all LoLUsers

    Returns:
        List[LoLUser]: all lol users
    """
    return session.query(LoLUser).all()


def get_lol_text_by_group(group_name: str) -> List[LoLText]:
    """
    Returns all text from a specific group

    Args:
        group_name (str): the name of the text group to query

    Returns:
        List[LoLText]: All the text that belongs to the given group
    """
    return session.query(LoLText).filter(LoLText.group == group_name).all()


def update_lol_user_last_updated(user: LoLUser, timestamp: int):
    """
    Updates a users last updated time

    Args:
        user (LoLuser): the user to update
        timestamp (int): the time in unix ms that the user
            was updated at
    """
    user.last_updated = timestamp
    session.commit()


def update_lol_user_winrate(user: LoLUser, game_result: GameResult):
    """
    Updates a given users winrate

    Note: currently only wins and losses are handled

    Args:
        user (LoLUser): the user to update
        game_result (GameResult): the result of the game
    """
    if game_result == GameResult.WIN:
        # user.wins = LoLUser.wins + 1
        session.query(LoLUser).filter(
            LoLUser.discord_id == user.discord_id
        ).update({"wins": user.wins + 1})
        session.commit()

    if game_result == GameResult.LOSS:
        # user.losses = LoLUser.losses + 1
        session.query(LoLUser).filter(
            LoLUser.discord_id == user.discord_id
        ).update({"losses": user.losses + 1})
        session.commit()


def set_lol_user_winrate(user: LoLUser, value: bool):
    """
    Sets winrate tracking for a given user

    Args:
        user (LoLUser): the user to enable winrate tracking for
        value (bool): True if winrate should be enabled, false otherwise
    """
    user.winrate = value
    session.commit()


def get_lol_users_with_winrate_enabled() -> List[LoLUser]:
    """
    Returns all users who currently have winrate enabled

    Returns:
        List[LoLUser]: any lol user who's winrate flag is
            set to true
    """
    return session.query(LoLUser).filter(LoLUser.winrate).all()


def create_new_lol_user(discord_id: int, riot_puuid: str):
    """
    Creates a new lol user with the given discord id and riot puuid

    Args:
        discord_id (int): the id of the discord user
        riot_puuid (str): the id of the riot account
    """
    user = LoLUser(discord_id, riot_puuid)
    session.add(user)
    session.commit()


def get_lol_user_by_discord_id(discord_id: int) -> LoLUser:
    """
    Returns the LoL user with the given discord id

    Args:
        discord_id (int): the discord id of the user to query

    Returns
        LoLUser: the lol user object with the given discord_id
    """
    try:
        return (
            session.query(LoLUser)
            .filter(LoLUser.discord_id == discord_id)
            .one()
        )
    except NoResultFound:
        return None


def reset_all_lol_user_winrate():
    """
    Resets the winrate of all LoLUsers to 0 - 0
    """
    session.query(LoLUser).update({"wins": 0, "losses": 0})
    session.commit()
