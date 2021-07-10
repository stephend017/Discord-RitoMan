"""
This class is where all database accessor functions will be defined
"""
from typing import List, Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import false

from discord_ritoman.models import GameResult
from discord_ritoman.db.schema import (
    LoLActiveGames,
    LoLBets,
    LoLText,
    LoLTextGroup,
    LoLUser,
)
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


def add_lol_user_points(user: LoLUser, points: int):
    """
    Adds points to a given user
    """
    session.query(LoLUser).filter(
        LoLUser.discord_id == user.discord_id
    ).update({"points": user.points + points})
    session.commit()


def add_lol_game(user: LoLUser, game_id: int, start_time: int, game_mode: str):
    """
    Adds an active lol game to the db
    """
    active_game = LoLActiveGames(
        game_id, user.discord_id, start_time, game_mode
    )
    session.add(active_game)
    session.commit()


def remove_lol_game(game_id: int, player_id: int):
    """
    Removes an active lol game from the db
    """
    session.query(LoLActiveGames).filter(
        LoLActiveGames.game_id == game_id, LoLActiveGames.player == player_id
    ).delete()
    session.commit()


def get_all_active_games():
    """
    Gets all the active games for all
    active discord ritoman users
    """
    return session.query(LoLActiveGames).all()


def get_all_active_bets():
    """
    Gets all the active bets for all
    active discord ritoman users
    """
    return session.query(LoLBets).filter(LoLBets.completed == false()).all()


def get_betters_on(user: LoLUser):
    """
    Gets all active bets on a given user
    """
    return (
        session.query(LoLBets)
        .filter(
            LoLBets.player == user.discord_id, LoLBets.completed == false()
        )
        .all()
    )


def create_bet(
    player: int, better: int, bet: int, prediction: bool, created: int
):
    """
    creates a new bet on a player
    """
    bet = LoLBets(player, better, bet, prediction, created)
    session.add(bet)
    session.commit()


def remove_bet(bet: LoLBets):
    """
    removes an active bet (marked as completed)
    """
    session.query(LoLBets).filter(
        LoLBets.player == bet.player, LoLBets.better == bet.better
    ).update({"completed": True})
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


def get_lol_user_by_discord_id(discord_id: int) -> Optional[LoLUser]:
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


def add_lol_text_group(group_name: str, group_description: str, user_id: int):
    """
    Adds a new text group with a description to the db

    Args:
        group_name (str): the name of the group being added (must be unique)
        group_description (str): a description of what this group is used for
        user_id (int): the discord id of the user adding the group
    """
    group = LoLTextGroup(group_name, group_description, user_id)
    session.add(group)
    session.commit()


def add_lol_text(group_name: str, content: str, user_id: int):
    """
    Adds a new text to the db

    Args:
        group_name (str): the name of the group being added (must be unique)
        content (str): the text to be displayed
        user_id (int): the discord id of the user adding the group
    """
    text = LoLText(group_name, content, user_id)
    session.add(text)
    session.commit()
