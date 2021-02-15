import datetime
import uuid

from discord_ritoman.utils import unix_time_millis
from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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

    def __init__(
        self, discord_id, riot_puuid, winrate=False, wins=0, losses=0
    ):
        self.discord_id = discord_id
        self.riot_puuid = riot_puuid
        self.last_updated = unix_time_millis(datetime.datetime.now())
        self.winrate = winrate
        self.wins = wins
        self.losses = losses


class LoLTextGroup(Base):
    """
    Definition of different types of LoL text being saved
    in this database. This is designed to scale
    """

    __tablename__ = "lol_text_group"
    # uuid = Column(
    #     String(32), primary_key=True
    # )  # UUID4 returns 32 character hex string
    name = Column(String(32), primary_key=True)
    usage = Column(String)
    # identifier = Column(String(8), unique=True)

    def __init__(self, name, usage):
        # self.uuid = uuid.uuid4().hex
        self.name = name
        self.usage = usage
        # self.identifier = identifier


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

    def __init__(self, group, content):
        self.uuid = uuid.uuid4().hex
        self.group = group
        self.content = content
