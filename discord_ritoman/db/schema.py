import datetime
import uuid

from discord_ritoman.utils import unix_time_millis
from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Integer, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LoLUser(Base):
    """
    Definition of discord user who uses this bot
    and plays LoL
    """

    __tablename__ = "lol_user"
    discord_id = Column(BigInteger, primary_key=True)
    winrate = Column(
        BigInteger,
        ForeignKey("lol_user_winrate.discord_id", ondelete="CASCADE"),
        nullable=True,
    )
    riot_puuid = Column(VARCHAR(255))
    last_updated = Column(BigInteger)

    def __init__(self, discord_id, riot_puuid):
        self.discord_id = discord_id
        self.riot_puuid = riot_puuid
        self.last_updated = unix_time_millis(datetime.datetime.now())


class LoLUserWinrate(Base):
    """
    Definition of discord user who wants this bot
    to record winrate
    """

    __tablename__ = "lol_user_winrate"
    discord_id = Column(BigInteger, primary_key=True)
    wins = Column(Integer)
    losses = Column(Integer)

    def __init__(self, discord_id):
        self.discord_id = discord_id
        self.wins = 0
        self.losses = 0


class LoLTextGroup(Base):
    """
    Definition of different types of LoL text being saved
    in this database. This is designed to scale
    """

    __tablename__ = "lol_text_group"
    uuid = Column(
        String(32), primary_key=True
    )  # UUID4 returns 32 character hex string
    name = Column(String(255), unique=True)
    usage = Column(String)

    def __init__(self, name, usage):
        self.uuid = uuid.uuid4().hex
        self.name = name
        self.usage = usage


class LoLText(Base):
    """
    Definition of all text used in this bot
    """

    __tablename__ = "lol_text"
    uuid = Column(
        String(32), primary_key=True
    )  # UUID4 returns 32 character hex string
    group = Column(String(32), ForeignKey("lol_text_group.uuid"))
    text = Column(String)

    def __init__(self, group, text):
        self.uuid = uuid.uuid4().hex
        self.group = group
        self.text = text