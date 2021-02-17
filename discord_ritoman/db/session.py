"""
Global store for the db session to use
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from discord_ritoman.utils import dynamic_import_class, get_db_uri

config_name = os.getenv("APP_CONFIG", "TestingConfig")
config = dynamic_import_class("discord_ritoman.db.config", config_name)
postgresql_engine = create_engine(
    get_db_uri(
        config.DB_URI_BASE,
        config.DB_USER,
        config.DB_PASS,
        config.DB_HOST,
        config.DB_PORT,
        config.DB_NAME,
    )
)
Session = sessionmaker(bind=postgresql_engine)
session = Session()
