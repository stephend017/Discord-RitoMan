import datetime
from typing import Any
import uuid

from discord_ritoman.utils import unix_time_millis
from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import (
    BigInteger,
    Boolean,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

Base: Any = declarative_base()


class LoLUser(Base):
    """
    Definition of discord user who uses this bot
    and plays LoL
    """

    __tablename__ = "lol_user"
    discord_id = Column(BigInteger, primary_key=True)
    riot_puuid = Column(String(255))
    last_updated = Column(BigInteger)
    winrate = Column(Boolean)
    wins = Column(Integer)
    losses = Column(Integer)
    points = Column(Integer)

    def __init__(
        self,
        discord_id: int,
        riot_puuid: str,
        winrate: bool = False,
        wins: int = 0,
        losses: int = 0,
        points: int = 1000,
    ):
        self.discord_id = discord_id
        self.riot_puuid = riot_puuid
        self.last_updated = unix_time_millis(datetime.datetime.now())
        self.winrate = winrate
        self.wins = wins
        self.losses = losses
        self.points = points


class LoLTextGroup(Base):
    """
    Definition of different types of LoL text being saved
    in this database. This is designed to scale
    """

    __tablename__ = "lol_text_group"
    name = Column(String(32), primary_key=True)
    usage = Column(String)
    modified = Column(DateTime)
    modified_by = Column(BigInteger)

    def __init__(self, name: str, usage: str, user: int):
        self.name = name
        self.usage = usage
        self.modified = datetime.datetime.now()
        self.modified_by = user


class LoLText(Base):
    """
    Definition of all text used in this bot
    """

    __tablename__ = "lol_text"
    uuid = Column(
        String(32), primary_key=True
    )  # UUID4 returns 32 character hex string
    group = Column(String(32), ForeignKey("lol_text_group.name"))
    content = Column(String)
    modified = Column(DateTime)
    modified_by = Column(BigInteger)

    def __init__(self, group: str, content: str, user: int):
        self.uuid = uuid.uuid4().hex
        self.group = group
        self.content = content
        self.modified = datetime.datetime.now()
        self.modified_by = user


class LoLActiveGames(Base):
    """
    Definition for active games being player by server members
    """

    __tablename__ = "lol_active_games"
    game_id = Column(BigInteger, primary_key=True)
    player = Column(BigInteger)
    start_time = Column(BigInteger)
    game_mode = Column(String)

    def __init__(
        self, game_id: int, player: int, start_time: int, game_mode: str
    ):
        self.game_id = game_id
        self.player = player
        self.start_time = start_time
        self.game_mode = game_mode


class LoLBets(Base):
    """
    Definition of bets
    """

    __tablename__ = "lol_bets"
    uuid = Column(
        String(32), primary_key=True
    )  # UUID4 returns 32 character hex string
    player = Column(BigInteger)
    better = Column(BigInteger)
    amount = Column(BigInteger)
    prediction = Column(Boolean)
    game_id = Column(BigInteger)

    def __init__(
        self,
        player: int,
        better: int,
        amount: int,
        prediction: bool,
        game_id: int,
    ):
        self.uuid = uuid.uuid4().hex
        self.player = player
        self.better = better
        self.amount = amount
        self.prediction = prediction
        self.game_id = game_id
